🧠 AI Classification

The system classifies each support email into one of the following intents:

Intent
Complaint
Feature Request
Bug Report
Refund Request
Billing Question
Technical Support
Account Issue
General Inquiry

Each classification also produces:

Confidence
Risk level
Priority
Reason

Example:

{
  "intent": "Refund Request",
  "confidence": 0.96,
  "risk": "MEDIUM",
  "priority": "MEDIUM",
  "reason": "Customer requests a refund for a damaged product."
}
🔀 Intelligent Routing

After classification, LangGraph routes the request to the appropriate workflow.

AUTO_REPLY

For safe requests, the system:

Customer Email
      ↓
Classification
      ↓
AUTO_REPLY
      ↓
Generate AI Response
      ↓
Send Gmail Reply
      ↓
Mark Email as Read
CREATE_TICKET

Requests requiring ticket creation are routed to the ticket workflow.

HUMAN_APPROVAL

Sensitive actions can be paused for human review:

Email
 ↓
Classification
 ↓
HUMAN_APPROVAL
 ↓
Pause Workflow
 ↓
Human Decision
 ↓
Approve / Reject
 ↓
Execute

LangGraph checkpointing allows the workflow state to be preserved during interruptions.

📧 Gmail Integration

The application integrates with Gmail using the Gmail API and OAuth 2.0.

It can:

Fetch unread emails
Extract sender and subject
Extract email body
Convert Gmail messages into application requests
Generate AI replies
Reply within the original Gmail thread
Mark processed emails as read
🤖 AI Reply Generation

For automatically handled emails, the system uses Groq to generate the response.

The workflow is:

Customer Email
      ↓
Groq Classification
      ↓
Router
      ↓
AUTO_REPLY
      ↓
Groq Reply Generation
      ↓
Gmail API
      ↓
Customer receives reply
📊 Evaluation

The project includes a 20-example classification evaluation dataset covering the supported intents and classification attributes.

Evaluation measures:

Intent accuracy
Risk accuracy
Priority accuracy
Average confidence
Classification report
Confusion matrix
Current evaluation result

Intent Classification Accuracy: 80%

The evaluation can be reproduced with:

python run_eval.py

The evaluation dataset is located at:

tests/eval_dataset.json

and the evaluation implementation is located in:

run_eval.py

Results are written to:

tests/results.txt
🖥️ Streamlit Dashboard

The Streamlit dashboard provides several pages for interacting with the system.

Configuration

Users can configure:

Groq API key
Gmail OAuth credentials
Gmail authentication
Inbox

The Inbox allows users to:

View unread Gmail messages
Process individual emails
Run the LangGraph workflow
Trigger automatic replies
Handle approval workflows
Approvals

Human approval requests can be reviewed and processed through the dashboard.

History

The History dashboard provides workflow statistics and displays:

Request ID
Sender
Source
Intent
Confidence
Risk
Route
Approval
Execution result
Error
Timestamp
⚡ FastAPI

The project also provides a FastAPI backend.

Swagger documentation:

FastAPI Swagger UI

The API provides a /process endpoint for processing support requests through the AutoOps workflow.

Example request structure:

{
  "source": "gmail",
  "sender": "customer@example.com",
  "subject": "Refund Request",
  "body": "I received a damaged product and would like a refund."
}
🐳 Docker

The application can be run locally using Docker Compose.

Build
docker compose build
Start
docker compose up

The local services are:

FastAPI:
http://localhost:8000/docs

Streamlit:
http://localhost:8501

Docker uses a shared application data directory:

/app/data

which contains the SQLite database and runtime Gmail files.

☁️ Railway Deployment

The application is deployed on Railway using two services:

Railway Project
│
├── FastAPI Service
│   └── AutoOps API
│
└── Streamlit Service
    └── AutoOps Dashboard
FastAPI

The FastAPI service provides the backend API.

Streamlit

The Streamlit service provides the interactive dashboard.

Persistent Storage

The Streamlit service uses a Railway persistent volume mounted at:

/app/data

This allows workflow history and Gmail authentication data to persist across container restarts.

🔐 Security

Sensitive files are intentionally excluded from GitHub:

.env
credentials.json
token.json
*.db
*.db-wal
*.db-shm
venv/

Gmail OAuth credentials and tokens are supplied to the deployed environment through Railway environment variables rather than being committed to the repository.

The repository does not contain:

Gmail credentials
Gmail OAuth tokens
Groq API keys
Local .env files
SQLite database files
📁 Project Structure
autoops-agent/
│
├── app/
│   ├── api/
│   │   ├── models.py
│   │   └── routes.py
│   │
│   ├── config/
│   │   └── runtime.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── graph/
│   │   ├── graph.py
│   │   ├── router.py
│   │   ├── state.py
│   │   ├── context.py
│   │   └── checkpointer.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── nodes/
│   │   ├── ingest.py
│   │   ├── classify.py
│   │   ├── execute.py
│   │   ├── approve.py
│   │   └── log.py
│   │
│   ├── prompts/
│   │   ├── classify_prompt.txt
│   │   └── reply_prompt.txt
│   │
│   ├── services/
│   │   ├── gmail_service.py
│   │   ├── groq_service.py
│   │   ├── sqlite_service.py
│   │   └── container.py
│   │
│   └── workers/
│       └── email_worker.py
│
├── tests/
│   ├── eval_dataset.json
│   ├── eval_dataset.py
│   ├── test_classification.py
│   └── results.txt
│
├── ui/
│   └── pages/
│       ├── configuration.py
│       ├── inbox.py
│       ├── approvals.py
│       └── history.py
│
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── main.py
├── run_eval.py
├── streamlit_app.py
├── requirements.txt
└── README.md
🛠️ Tech Stack
AI / LLM
Groq
Llama 3.3 70B
LangGraph
LangChain ecosystem
Backend
Python
FastAPI
Pydantic
Frontend
Streamlit
Automation
Gmail API
Gmail OAuth 2.0
Database
SQLite
LangGraph SQLite checkpointing
Reliability
Tenacity
Retry mechanisms
Workflow checkpointing
Deployment
Docker
Docker Compose
Railway
GitHub
Evaluation
scikit-learn
Accuracy
Classification report
Confusion matrix
🚀 Run Locally
1. Clone the repository
git clone https://github.com/hunter312-ts/autoops-agent.git
cd autoops-agent
2. Create virtual environment

Windows:

python -m venv venv

Activate:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key

Never commit .env.

5. Run FastAPI
uvicorn main:app --reload

Open:

http://localhost:8000/docs
6. Run Streamlit

In another terminal:

streamlit run streamlit_app.py

Open:

http://localhost:8501
🧪 Run Evaluation

Run:

python run_eval.py

The evaluation uses the 20-example dataset:

tests/eval_dataset.json

and reports classification performance including intent accuracy.

Current intent accuracy:

80%
🔮 Future Improvements

Potential improvements include:

PostgreSQL for multi-service persistent storage
Production OAuth callback flow
More extensive evaluation datasets
Automated regression testing
Additional support integrations
Real ticketing-system integration
Better observability and monitoring
Background Gmail polling
Multi-user authentication
Production-grade deployment architecture
👨‍💻 Project

AutoOps Agent demonstrates an end-to-end AI automation workflow combining LLMs, LangGraph, Gmail, human-in-the-loop workflows, FastAPI, Streamlit, Docker, and cloud deployment.

Live Application

🚀 AutoOps Streamlit Dashboard

API

⚡ AutoOps FastAPI Documentation

Source Code

GitHub Repository — hunter312-ts/autoops-agent

Live_URL: https://diligent-luck-production-1d85.up.railway.app/