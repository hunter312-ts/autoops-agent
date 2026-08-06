from pathlib import Path

from pydantic import BaseModel


class ProcessRequest(BaseModel):
    source: str
    sender: str
    subject: str
    body: str

    groq_api_key: str

    gmail_credentials_path: str = "credentials.json"
    gmail_token_path: str = "token.json"