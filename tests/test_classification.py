from pathlib import Path
import os

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from app.config.runtime import RuntimeConfig
from app.models.schemas import SupportRequest
from app.services.groq_service import GroqService
from tests.eval_dataset import EVAL_DATASET


def run_evaluation():
    """
    Run the AutoOps classification evaluation.

    Evaluates:
    - Intent accuracy
    - Risk accuracy
    - Priority accuracy
    - Average confidence
    - Intent classification report
    - Intent confusion matrix
    """

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY environment variable is not set."
        )

    runtime_config = RuntimeConfig(
        groq_api_key=groq_api_key,
        gmail_credentials_path=Path("credentials.json"),
        gmail_token_path=Path("token.json"),
    )

    groq = GroqService(runtime_config)

    # --------------------------------------------------
    # Dataset
    # --------------------------------------------------

    dataset = EVAL_DATASET

    print("=" * 60)
    print("Running AutoOps Classification Evaluation")
    print("=" * 60)

    print(f"Dataset size: {len(dataset)}")
    print()

    # --------------------------------------------------
    # Storage
    # --------------------------------------------------

    true_intents = []
    predicted_intents = []

    true_risks = []
    predicted_risks = []

    true_priorities = []
    predicted_priorities = []

    confidences = []

    # --------------------------------------------------
    # Run Evaluation
    # --------------------------------------------------

    for i, sample in enumerate(dataset, start=1):

        request = SupportRequest(
            request_id=f"TEST-{i:03d}",
            source="gmail",
            sender="tester@example.com",
            subject=sample["subject"],
            body=sample["body"],
        )

        try:

            prediction = groq.classify(request)

        except Exception as e:

            print(
                f"[{i:02d}] ERROR - "
                f"{sample['subject']}: {e}"
            )

            continue

        # --------------------------------------------------
        # Intent
        # --------------------------------------------------

        expected_intent = sample["expected"]["intent"]
        predicted_intent = prediction.intent

        true_intents.append(expected_intent)
        predicted_intents.append(predicted_intent)

        # --------------------------------------------------
        # Risk
        # --------------------------------------------------

        true_risks.append(
            sample["expected"]["risk"]
        )

        predicted_risks.append(
            prediction.risk
        )

        # --------------------------------------------------
        # Priority
        # --------------------------------------------------

        true_priorities.append(
            sample["expected"]["priority"]
        )

        predicted_priorities.append(
            prediction.priority
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        confidences.append(
            prediction.confidence
        )

        # --------------------------------------------------
        # Result
        # --------------------------------------------------

        correct = (
            expected_intent == predicted_intent
        )

        status = "PASS" if correct else "FAIL"

        print(
            f"[{i:02d}] "
            f"{status:<5} "
            f"Expected: {expected_intent:<20} "
            f"Predicted: {predicted_intent}"
        )

    # --------------------------------------------------
    # Check Results
    # --------------------------------------------------

    if not true_intents:

        raise RuntimeError(
            "No successful evaluation results were produced."
        )

    # --------------------------------------------------
    # Metrics
    # --------------------------------------------------

    intent_accuracy = accuracy_score(
        true_intents,
        predicted_intents,
    )

    risk_accuracy = accuracy_score(
        true_risks,
        predicted_risks,
    )

    priority_accuracy = accuracy_score(
        true_priorities,
        predicted_priorities,
    )

    average_confidence = (
        sum(confidences) / len(confidences)
    )

    report = classification_report(
        true_intents,
        predicted_intents,
        zero_division=0,
    )

    matrix = confusion_matrix(
        true_intents,
        predicted_intents,
    )

    # --------------------------------------------------
    # Display Results
    # --------------------------------------------------

    print()
    print("=" * 60)

    print(
        f"Successful Samples : {len(true_intents)}/{len(dataset)}"
    )

    print(
        f"Intent Accuracy    : {intent_accuracy:.2%}"
    )

    print(
        f"Risk Accuracy      : {risk_accuracy:.2%}"
    )

    print(
        f"Priority Accuracy  : {priority_accuracy:.2%}"
    )

    print(
        f"Average Confidence : {average_confidence:.2f}"
    )

    print("=" * 60)

    print()
    print("Classification Report")
    print()

    print(report)

    print("Confusion Matrix")
    print()

    print(matrix)

    # --------------------------------------------------
    # Save Results
    # --------------------------------------------------

    results_path = Path(
        "tests/results.txt"
    )

    with open(
        results_path,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(
            "AutoOps Classification Evaluation\n"
        )

        f.write("=" * 50 + "\n\n")

        f.write(
            f"Dataset Size       : {len(dataset)}\n"
        )

        f.write(
            f"Successful Samples : {len(true_intents)}\n\n"
        )

        f.write(
            f"Intent Accuracy    : {intent_accuracy:.2%}\n"
        )

        f.write(
            f"Risk Accuracy      : {risk_accuracy:.2%}\n"
        )

        f.write(
            f"Priority Accuracy  : {priority_accuracy:.2%}\n"
        )

        f.write(
            f"Average Confidence : {average_confidence:.2f}\n\n"
        )

        f.write(
            "Classification Report\n"
        )

        f.write(report)

        f.write(
            "\n\nConfusion Matrix\n"
        )

        f.write(str(matrix))

    print()
    print(
        f"Results saved to {results_path}"
    )

    return {
        "intent_accuracy": intent_accuracy,
        "risk_accuracy": risk_accuracy,
        "priority_accuracy": priority_accuracy,
        "average_confidence": average_confidence,
        "samples": len(dataset),
        "successful_samples": len(true_intents),
    }


# --------------------------------------------------
# Direct Execution
# --------------------------------------------------

if __name__ == "__main__":
    run_evaluation()