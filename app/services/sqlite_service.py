from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)
import sqlite3
from pathlib import Path

from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logging import logger
from app.graph import state
class SQLiteService:
    """
    Handles all SQLite database operations.
    """
    def __init__(self):
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.initialize_database()
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    def initialize_database(self):
        """
        Create database tables if they do not exist.
        """
        logger.info("Initializing SQLite database...")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS workflow_logs (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    request_id TEXT,

                    source TEXT,

                    sender TEXT,

                    intent TEXT,

                    confidence REAL,

                    risk TEXT,

                    route TEXT,

                    approval TEXT,

                    execution_result TEXT,

                    error TEXT,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                )
                """
            )
            conn.commit()
        logger.info("SQLite database initialized.")

    @retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=5),
    reraise=True,
    )
    def save_workflow(self, state):
         """
    Save one workflow execution.
    """
         request = state.get("request")
         classification = state.get("classification")

         with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
            """
            INSERT INTO workflow_logs(

                request_id,
                source,
                sender,
                intent,
                confidence,
                risk,
                route,
                approval,
                execution_result,
                error
            )
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                request.request_id if request else None,
                request.source if request else None,
                request.sender if request else None,
                classification.intent if classification else None,
                classification.confidence if classification else None,
                classification.risk if classification else None,
                state.get("route"),
                state.get("approval"),
                state.get("execution_result"),
                state.get("error"),
            ),
        )

            conn.commit()

    logger.info("Workflow saved to SQLite.")

sqlite_service = SQLiteService()