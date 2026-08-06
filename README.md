# 🤖 AutoOps AI

> AI-powered customer support automation using **LangGraph**, **FastAPI**, **Groq**, **Gmail API**, **SQLite**, and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![LangGraph](https://img.shields.io/badge/LangGraph-1.x-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-blue)

---

# 📌 Overview

AutoOps AI is an intelligent customer support automation platform.

The system automatically:

- Reads unread Gmail messages
- Uses an LLM (Groq) to classify requests
- Decides the appropriate workflow using LangGraph
- Automatically replies to low-risk emails
- Creates support tickets
- Sends high-risk requests for human approval
- Stores every workflow in SQLite
- Visualizes everything through a Streamlit dashboard

---

# 🚀 Features

- Gmail Integration
- LangGraph Stateful Workflows
- Human-in-the-Loop Approval
- Runtime Dependency Injection
- SQLite Workflow Logging
- Retry Logic (Tenacity)
- FastAPI Backend
- Streamlit Dashboard
- Runtime API Key Configuration
- Modular Service Architecture

---

# 🏗 System Architecture

```

                    ┌────────────────────┐
                    │    Streamlit UI    │
                    └─────────┬──────────┘
                              │
                              ▼
                     Runtime Configuration
                              │
                              ▼
                    Service Container
                              │
        ┌─────────────────────┼────────────────────┐
        ▼                     ▼                    ▼
   Groq Service         Gmail Service        SQLite Service
        │                     │                    │
        └──────────────┬──────┴────────────────────┘
                       ▼
                 LangGraph Workflow
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     AUTO_REPLY   CREATE_TICKET  HUMAN_APPROVAL
                       │
                       ▼
                Streamlit Approval UI

# workflow
Unread Gmail

↓

Ingest Node

↓

Classification Node

↓

Router

↓

AUTO_REPLY
CREATE_TICKET
HUMAN_APPROVAL

↓

Log Node

↓

SQLite

↓

Dashboard

## Project Structure
autoops-agent/

app/
│
├── config/
├── core/
├── graph/
├── models/
├── nodes/
├── prompts/
├── routers/
├── services/
│
├── gmail_service.py
├── groq_service.py
├── sqlite_service.py
│
ui/
│
├── pages/
│   ├── configuration.py
│   ├── inbox.py
│   ├── approvals.py
│   └── history.py
│
streamlit_app.py
main.py

# ⚙ Technologies
| Technology | Purpose            |
| ---------- | ------------------ |
| Python     | Backend            |
| FastAPI    | REST API           |
| LangGraph  | AI Workflow Engine |
| Groq       | LLM                |
| Gmail API  | Email Automation   |
| SQLite     | Persistence        |
| Streamlit  | Dashboard          |
| Tenacity   | Retry Logic        |

# 📊 Architecture Diagram
                AutoOps AI

        Streamlit Dashboard
                │
      Runtime Configuration
                │
                ▼
        Service Container
     ┌──────────┼──────────┐
     │          │          │
     ▼          ▼          ▼
   Groq      Gmail      SQLite
     │          │          │
     └──────────┴──────────┘
                │
                ▼
           LangGraph
                │
      ┌─────────┼─────────┐
      ▼         ▼         ▼
 AUTO_REPLY  CREATE_TICKET  HUMAN_APPROVAL
                │
                ▼
            Workflow Log


# API Example
-POST /process
{
    "source":"gmail",
    "sender":"john@gmail.com",
    "subject":"Refund Request",
    "body":"Product arrived damaged.",
    "groq_api_key":"...",
    "gmail_credentials_path":"credentials.json",
    "gmail_token_path":"token.json"
}

# Installation
git clone https://github.com/yourname/autoops-ai.git

cd autoops-ai

python -m venv venv

pip install -r requirements.txt

# Future Improvements
-Docker Deployment
-PostgreSQL
-Redis Queue
-Background Workers
-OAuth Login
-Multi-user Support
-Slack Integration
-Outlook Integration
-LangSmith Tracing

Author
Muhammad Tayyab Sattar
MS Intelligent Data Science
National Yunlin University of Science and Technology
Taiwan