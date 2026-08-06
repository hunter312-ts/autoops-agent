import token

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from googleapiclient.errors import HttpError
from pathlib import Path
import os
import base64
from email.header import decode_header
from app.config.runtime import RuntimeConfig
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.core.logging import logger


# Gmail permissions
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]


class GmailService:
    """
    Handles Gmail authentication and operations.
    """

    def __init__(self,config: RuntimeConfig):
        self.config = config

        self.credentials_path = config.gmail_credentials_path

        self.token_path = config.gmail_token_path

        self.service = None


    
    @retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
    reraise=True,
    )
    def authenticate(self):
        """
        Authenticate with Gmail using OAuth2.
        """
        logger.info("Authenticating with Gmail...")
        creds = None
        #token_path = "token.json"
        #credentials_path = "credentials.json"
        # Load existing token if available
        if self.credentials_path is None:
            raise ValueError(
                        "gmail_credentials_path is not configured."
    )

        if self.token_path is None:
            raise ValueError(
                       "gmail_token_path is not configured."
    )
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(
                str(self.token_path),
                SCOPES,
            )

        # If token is missing or expired
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing Gmail token...")
                creds.refresh(Request())
            else:
                logger.info("Opening browser for Gmail login...")
                flow = InstalledAppFlow.from_client_secrets_file(
    str(self.credentials_path),
    SCOPES,
)
                creds = flow.run_local_server(port=0)
            # Save token
            with open(str(self.token_path), "w") as token:
                token.write(creds.to_json())
        self.service = build(
            "gmail",
            "v1",
            credentials=creds,
        )
        logger.info("Gmail authentication successful.")
        return self.service

    
    @retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
    reraise=True,
    )
    def fetch_unread_emails(self, max_results: int = 5):
            """
            Fetch unread Gmail messages.
            """
            if self.service is None:
                                        raise RuntimeError(
                                "GmailService.authenticate() must be called first."
                            )
            logger.info("Fetching unread emails...")

            results = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    labelIds=["INBOX"],
                    q="is:unread",
                    maxResults=max_results,
                )
                .execute()
            )

            messages = results.get("messages", [])

            emails = []

            for message in messages:

                msg = (
                    self.service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=message["id"],
                        format="full",
                    )
                    .execute()
                )

                headers = msg["payload"]["headers"]

                subject = ""
                sender = ""

                for header in headers:

                    if header["name"] == "Subject":
                        subject = header["value"]

                    elif header["name"] == "From":
                        sender = header["value"]

                body = ""

                if "parts" in msg["payload"]:

                    for part in msg["payload"]["parts"]:

                        if part["mimeType"] == "text/plain":

                            data = part["body"]["data"]

                            body = base64.urlsafe_b64decode(data).decode("utf-8")

                            break

                elif "body" in msg["payload"]:

                    data = msg["payload"]["body"].get("data")

                    if data:

                        body = base64.urlsafe_b64decode(data).decode("utf-8")

                emails.append(
                    {
                        "id": message["id"],
                        "sender": sender,
                        "subject": subject,
                        "body": body,
                    }
                )

            logger.info(f"Fetched {len(emails)} unread emails.")

            return emails
    def convert_to_raw_request(self, email:dict,) -> dict:
        """
        Convert Gmail email to our standard raw_request format.
        """

        return {
            "source": "gmail",
            "sender": email["sender"],
            "subject": email["subject"],
            "body": email["body"],
        }

    @retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(HttpError),
    reraise=True,
    )
    def mark_as_processed(self, message_id: str):
        """
        Mark a Gmail message as read by removing the UNREAD label.
        """
        if self.service is None:
          raise RuntimeError("GmailService.authenticate() must be called first.")
        logger.info(f"Marking email {message_id} as processed...")
        try:
            self.service.users().messages().modify(
                userId="me",
                id=message_id,
                body={
                    "removeLabelIds": ["UNREAD"]
                },
            ).execute()
            logger.info("Email marked as read successfully.")
        except Exception as e:
            logger.error(f"Failed to mark email as processed: {e}")
            raise

