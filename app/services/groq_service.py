from pathlib import Path
import json

from groq import Groq

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)

from app.config.runtime import RuntimeConfig
from app.core.logging import logger
from app.models.schemas import (
    SupportRequest,
    ClassificationResult,
)


class GroqService:
    """
    Handles all communication with the Groq API.

    The service is configured at runtime using a
    RuntimeConfig object instead of reading API keys
    from .env.
    """

    def __init__(self, config: RuntimeConfig):

        self.config = config

        self.client = Groq(
            api_key=config.groq_api_key
        )

        self.model = config.model

    # ---------------------------------------------------------

    @staticmethod
    def load_prompt(prompt_name: str) -> str:
        """
        Load a prompt from the prompts directory.
        """

        prompt_path = Path("app/prompts") / prompt_name

        return prompt_path.read_text(
            encoding="utf-8"
        )

    # ---------------------------------------------------------

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,
            min=2,
            max=10,
        ),
        reraise=True,
    )
    def classify(
        self,
        request: SupportRequest,
    ) -> ClassificationResult:
        """
        Classify a support request using Groq.
        """

        system_prompt = self.load_prompt(
            "classify_prompt.txt"
        )

        user_prompt = f"""
Subject:
{request.subject}

Message:
{request.body}
"""

        logger.info(
            f"Classifying request {request.request_id}..."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        logger.info("Groq response received.")

        raw_json = response.choices[0].message.content

        try:

            parsed = json.loads(raw_json)

            return ClassificationResult(**parsed)

        except Exception as e:

            logger.error(
                f"Classification parsing failed: {e}"
            )

            raise