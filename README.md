## StackExplain

Explain Python error messages using LLMs.

## Description 
StackExplain is a website, backend API, and CLI tool that analyzes Python error messages and explains what causes them using large language models. It suggests fixes and includes relevant links to documentation.

## Installation (Development)

Clone the repository:
```
git clone https://github.com/adityapatwardhan1/stackexplain.git
```

Build the virtual environment and install dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the backend server:
```
cd backend/src/stackexplain
uvicorn app.main:app --reload
```

To run the frontend site:
```
cd frontend
npm install
npm run dev
```

To build the CLI tool:
```
cd backend
pip install -e .
```