# GeminiLLM

This repository contains five small demo scripts that showcase chat, vision,
multilingual, and PDF Q&A workflows using Google Generative AI integrations with
LangChain.

Projects
--------

- `1-chat.py` — Simple text chat demo using the configured chat model.
- `2-vision.py` — Vision demo demonstrating image processing and visual prompts.
- `3-qachat.py` — Conversational question-answering demo.
- `4-multilang.py` — Multilingual prompt/response demo.
- `5-multipdf.py` — upload multiple PDFs, embed content, and run
	similarity-search + QA.

Prerequisites
-------------

- Python 3.10+ recommended.
- A Google API key with access to the GenAI services (set `GOOGLE_API_KEY`).

Virtual environment (Windows)
-----------------------------

1. Create a `venv` virtual environment (this repo keeps `venv` by convention):

```powershell
python -m venv venv
```

2. Activate the virtual environment:

```powershell
# PowerShell
venv\Scripts\Activate.ps1

# Command Prompt
venv\Scripts\activate.bat
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

Running the demos
-----------------

- Chat demo:

```powershell
streamlit 1-chat.py
```

- Vision demo:

```powershell
streamlit 2-vision.py
```

- QA Chat demo:

```powershell
streamlit 3-qachat.py
```

- Multilingual demo:

```powershell
streamlit 4-multilang.py
```

- Multiple-PDF Q&A (Streamlit):

```powershell
streamlit run 5-multipdf.py
```

Environment variables
---------------------

- Create a `.env` file or set environment variables for keys like:

```
GOOGLE_API_KEY=your_api_key_here
EMBEDDING_MODEL=models/embedding-gecko-001  # optional override
```

Notes about `.venv` and cleaning
--------------------------------

- You indicated `venv` and `vector_store/` are important; I removed temporary
	helper scripts from the repo. I attempted to delete `.venv` but Windows
	reported permission errors (files in use). To remove `.venv` safely, deactivate
	any active virtual environments and ensure no processes are using files from
	that folder, then remove it manually or run:

```powershell
deactivate  # if activated
Remove-Item -LiteralPath .venv -Recurse -Force
```

Keeping `vector_store/`
----------------------

- The `vector_store/` directory contains persisted FAISS indices used by
	`5-multipdf.py`. Do not delete it unless you want to re-process PDFs.

If you want further cleanup (remove `venv` and re-create a single clean venv,
or produce macOS/Linux instructions), tell me which OS and I'll make the changes.


