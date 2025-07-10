---
title: LectureLensSpace
emoji: 🏃
colorFrom: red
colorTo: blue
sdk: streamlit
pinned: false
license: mit
short_description: This is hugging face space for the lecture lens project
sdk_version: 1.46.1
---



# 🧑🏽‍🏫 LectureLens

**LectureLens** is a LangChain-powered app for summarizing content from **YouTube videos** and **web URLs**, enabling quick note generation and content summarization from both video and text.

---

## 🔍 Features

* 🎥 YouTube video summarization using `YoutubeLoader`
* 🌐 Webpage summarization using `UnstructuredURLLoader`
* ⚡ Powered by LLaMA3-8B via ChatGroq for rapid and intelligent text generation
* 🔧 Designed for ease of extension with other loaders like Selenium-based scrapers

---

## 🧠 Why Use Custom Headers?

Some websites block or alter content for non-browser clients (like Python scripts). To avoid this, `UnstructuredURLLoader` uses custom HTTP headers like:

```http
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
```

This helps prevent:

* ❌ `403 Forbidden` errors
* ❌ CAPTCHA interruptions
* ❌ Incomplete HTML loads

---

## ⚙️ Loaders Used

| Loader Type             | Purpose                                   |
| ----------------------- | ----------------------------------------- |
| `YoutubeLoader`         | Summarizes spoken content from videos     |
| `UnstructuredURLLoader` | Extracts & summarizes static webpage HTML |
| *(Optional)* Selenium   | Handles JavaScript-heavy dynamic pages    |

---

## 🚀 Quick Start

1. Clone this repo
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

---

## 🧱 Built With

* [LangChain](https://python.langchain.com/)
* [ChatGroq + LLaMA3](https://groq.com/)
* [Unstructured.io](https://github.com/Unstructured-IO/unstructured)
* [Streamlit](https://streamlit.io/)
* [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/)

---

## 📌 To-Do

* [ ] Add transcript language support
* [ ] Add Selenium fallback for JavaScript websites
* [ ] Export summaries as PDF or Markdown
