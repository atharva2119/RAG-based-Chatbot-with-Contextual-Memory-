# Pluggable Chatbot with Contextual Memory

A customizable chatbot powered by [LangChain](https://github.com/langchain-ai/langchain), [Ollama](https://github.com/jmorganca/ollama) local LLMs, and a vector database. It can ingest any dataset (e.g., CSV, PDFs, text), build embeddings, and maintain conversational context and memory across sessions.

---

## 🔧 Prerequisites

- **Python 3.11 or lower**\
  LangChain-Chroma currently requires Python ≤3.11 for pre-built binaries. If you use Python 3.12 or newer, you may encounter build errors during `pip install`.

- **Ollama CLI installed**\
  Install from [https://ollama.com](https://ollama.com).

- **Local Ollama models**\
  Before running the bot, pull the following models locally:

  ```bash
  ollama pull llama
  ollama pull mxbai-embed-large
  ```

  - `llama` — your chosen LLM for chat (e.g. `llama2`, smaller local model)
  - `mxbai-embed-large` — embedding model for vectorization

---

## 📁 File Structure

```
pluggable-chatbot/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── main.py                    # Streamlit app entry point and chatbot logic
├── working.py                 # Headless script without Streamlit
├── data.csv                   # Sample data source
├── vector.py                  # CSV to vector DB logic
└── vector_db/                 # Persisted vector database
```

---

## ⚙️ Setup & Installation

1. **Clone this repository**

   ```bash
   git clone <your-repo-url>
   cd pluggable-chatbot
   ```

2. **Create a virtual environment** (using Python 3.11 or lower)

   ```bash
   py -3.11 -m venv env
   .\env\Scripts\activate     # Windows PowerShell
   # or source env/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Pull Ollama models**

   ```bash
   ollama pull llama
   ollama pull mxbai-embed-large
   ```

---

## 🚀 Running the Chatbot

To start the Streamlit interface:

```bash
streamlit run main.py
```

Open the displayed `localhost:` URL in your browser. You can upload new data files on the sidebar, ask questions, and see how the bot maintains context and retrieves relevant information.

---

---

## 🏗️ Implementation

All functionality — data ingestion, embedding, retrieval, LLM interaction, and conversational memory — is implemented directly in `main.py`. There are no separate modules; the Streamlit app serves as the sole entry point and orchestrator of the chatbot logic.

---

## 📝 Headless Script (`working.py`)

The `working.py` file replicates the chatbot's core features without the Streamlit frontend. It can be run in any terminal:

```bash
python working.py
```

Inside `working.py`, the script:

1. **Loads** `data.csv` via `vector.py` to create or load the vector database.
2. **Initializes** the `mxbai-embed-large` embedding model and builds or retrieves embeddings using Chroma.
3. **Sets up** the Ollama LLM (`llama`) alongside a LangChain conversation memory buffer.
4. **Starts** a console-based REPL loop, prompting the user for queries and returning responses while preserving chat history.

## 🙏 Conclusion

Thank you for checking out the Pluggable Chatbot project! This repository provides both a user-friendly Streamlit interface (`main.py`) and a headless Python script (`working.py`) so you can integrate the core chatbot logic into your own applications or workflows.

Feel free to customize the data source, LLM models, or embedding parameters to suit your needs. We hope this project accelerates your development of conversational AI solutions with LangChain and Ollama.

*Happy coding and conversational building!* 🎉

---

## 🤝 Contributing & Testing

- **Fork** the repo, make changes in `main.py`, `working.py`, or `vector.py`, and submit a PR.
- (Optional) **Add basic tests** and ensure they pass before creating the PR. 