# Mental Health CBT Chatbot (T-Bot)

A guided **Cognitive Behavioural Therapy (CBT)** chatbot that walks a user through a
7-column *thought record* exercise, backed by a fine-tuned language model and served
over a FastAPI HTTP API.

> ⚠️ **Not a medical device.** This is an educational project. It includes a
> rule-based crisis-detection protocol that surfaces hotline information, but it is
> not a substitute for professional mental-health care.

## Features

- **Guided thought records** — steps the user through the CBT thought-record columns.
- **Crisis safety protocol** — rule-based keyword detection that always runs first and
  returns hotline/text-line resources (e.g. 988, Crisis Text Line).
- **FastAPI service** — simple `/chat` endpoint with per-user sessions.
- **Fine-tuning pipeline** — scripts for synthetic data generation, preprocessing, and
  fine-tuning an LLM for empathetic, on-task responses.

## Project structure

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI application exposing the `/chat` endpoint. |
| `thought_record_bot_final.py` | Core `ThoughtRecordBot` conversation logic + crisis protocol. |
| `Synthetic_data_generator.py` | Generates synthetic CBT dialogue training data via an LLM API. |
| `data_preprocessor.py` | Cleans/formats the dataset for fine-tuning. |
| `finetune_chatbot.py` | Fine-tuning pipeline for the base LLM. |

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic
```

Set the LLM API key used by the data generator as an environment variable:

```bash
export YOUR_POWERFUL_LLM_API_KEY="your-key-here"
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Then send a message:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u1", "message": "I keep thinking I will fail my exam."}'
```
