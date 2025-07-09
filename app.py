import streamlit as st
import validators
import logging
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader,SeleniumURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# ---------------------- Setup Logging --------------------------
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ---------------------- Streamlit UI --------------------------
st.set_page_config('🧑🏽‍🏫LectureLens')
st.title('LectureLens')

with st.sidebar:
    groq_api_key = st.text_input('groq token', type='password')

options = ['Other Text url', 'Youtube Link']
method = st.radio('Method', options=options, index=0)

if not (method and groq_api_key):
    st.warning('Please enter complete details and choose preferred method')
else:
    link = st.text_input('Enter url')
    summarize = st.button('Summarize')
    llm = ChatGroq(model='meta-llama/llama-4-scout-17b-16e-instruct', groq_api_key=groq_api_key)

    prompt_template = '''
    Provide summary of following text in 200 words.
    
    {text}
    '''
    prompt = PromptTemplate(template=prompt_template, input_variables=['text'])

    if summarize:
        if not validators.url(link):
            st.warning('Enter a valid URL first')
        else:
            index = options.index(method)
            try:
                with st.spinner('Loading and summarizing text...'):
                    logger.info(f"Selected Method Index: {index}")
                    logger.info(f"URL: {link}")

                    if index == 0:
                        try:
                            loader = SeleniumURLLoader(
                                urls=[link],
                                # ssl_verify=False,
                                # headers={
                                #     "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
                                # }
                            )
                        except Exception as loader_error:
                            logger.exception("Error creating UnstructuredURLLoader")
                            st.error(f"Loader creation error: {loader_error}")
                            st.stop()
                    else:
                        try:
                            loader = YoutubeLoader.from_youtube_url(
                                youtube_url=link, add_video_info=False
                            )
                        except Exception as yt_loader_error:
                            logger.exception("Error creating YoutubeLoader")
                            st.error(f"YouTube loader error: {yt_loader_error}")
                            st.stop()

                    try:
                        logger.info("Calling loader.load()...")
                        docs = loader.load()
                        logger.info(f"Documents loaded: {len(docs)}")
                    except Exception as load_error:
                        logger.exception("Error loading documents")
                        st.error(f"Document loading error: {load_error}")
                        st.stop()


                    if not docs:
                        st.error("No content found at the provided URL.")
                        st.stop()

                    splitter = RecursiveCharacterTextSplitter(chunk_size=1999, chunk_overlap=199)
                    final_docs = splitter.split_documents(docs)

                    chain = load_summarize_chain(
                        llm=llm,
                        chain_type='refine',
                        # prompt=prompt            #notrequired in refine chain
                        verbose=True
                    )
                    summary = chain.run(final_docs)
                    st.success(summary)

            except Exception as e:
                logger.exception("Unhandled Exception")
                st.exception(f"An error occurred: {str(e)}")
