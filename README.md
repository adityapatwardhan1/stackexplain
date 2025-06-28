## StackExplain

Explain Python error messages using LLMs.

## Description 
StackExplain is a website + backend API that analyzes Python error messages and explains what causes them using large language models. It suggests fixes and includes relevant links to documentation.

## Features

- 📋 Understand Python error messages instantly
- 🛠️ Suggested fixes and debugging help
- 🔗 Relevant documentation links
- 🧠 Powered by OpenRouter + OpenAI-compatible models
- 🧪 Easily extendable to other languages or a web UI

## Installation (Development)

Clone the repo and install locally:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the backend server:
```
cd backend
uvicorn app.main:app --reload
```

To run the frontend site:
```
cd frontend
npm install
npm run dev
```