#from tests.test_classification import run_evaluation
#if __name__ == "__main__":
#    run_evaluation()

##Note: To run this evaluation script, you must set the GROQ_API_KEY environment variable with your Groq API key. For example:
# export GROQ_API_KEY=your_key_here
# python run_eval.py -> this will run the evaluation and write the results to tests/results.txt
"""
run_eval.py

Runs the AutoOps classifier against the labeled evaluation
dataset in tests/eval_dataset.py, measures accuracy on
intent / risk / priority, and writes a report to
tests/results.txt (and prints it to stdout).

Usage:
    python run_eval.py

Requires GROQ_API_KEY to be set in the environment.
"""

import os
import sys
import time
import uuid

from sklearn.metrics import classification_report, confusion_matrix

from app.config.runtime import RuntimeConfig
from app.models.schemas import SupportRequest
from app.services.groq_service import GroqService
from tests.eval_dataset import EVAL_DATASET


def build_groq_service() -> GroqService:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY is not set in the environment.")
        sys.exit(1)

    config = RuntimeConfig(
        groq_api_key=api_key,
        model=os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
    )
    return GroqService(config)


def run_eval():
    groq = build_groq_service()

    y_true_intent, y_pred_intent = [], []
    y_true_risk, y_pred_risk = [], []
    y_true_priority, y_pred_priority = [], []
    confidences = []
    failures = []

    total = len(EVAL_DATASET)

    for i, sample in enumerate(EVAL_DATASET, start=1):
        request = SupportRequest(
            request_id=str(uuid.uuid4()),
            source="webhook",
            sender="eval@autoops.local",
            subject=sample["subject"],
            body=sample["body"],
        )

        expected = sample["expected"]

        print(f"[{i}/{total}] Classifying: {sample['subject']!r}...")

        try:
            result = groq.classify(request)
        except Exception as e:
            print(f"  -> FAILED: {e}")
            failures.append({"subject": sample["subject"], "error": str(e)})
            continue

        y_true_intent.append(expected["intent"])
        y_pred_intent.append(result.intent)

        y_true_risk.append(expected["risk"])
        y_pred_risk.append(result.risk)

        y_true_priority.append(expected["priority"])
        y_pred_priority.append(result.priority)

        confidences.append(result.confidence)

        # Groq free tier is rate-limited; a small delay avoids 429s.
        time.sleep(0.5)

    if not y_true_intent:
        print("No samples were successfully classified. Aborting.")
        sys.exit(1)

    intent_acc = sum(
        t == p for t, p in zip(y_true_intent, y_pred_intent)
    ) / len(y_true_intent)

    risk_acc = sum(
        t == p for t, p in zip(y_true_risk, y_pred_risk)
    ) / len(y_true_risk)

    priority_acc = sum(
        t == p for t, p in zip(y_true_priority, y_pred_priority)
    ) / len(y_true_priority)

    avg_confidence = sum(confidences) / len(confidences)

    intent_labels = sorted(set(y_true_intent) | set(y_pred_intent))
    report = classification_report(
        y_true_intent,
        y_pred_intent,
        labels=intent_labels,
        zero_division=0,
    )
    cm = confusion_matrix(y_true_intent, y_pred_intent, labels=intent_labels)

    lines = []
    lines.append("AutoOps Classification Evaluation")
    lines.append("=" * 50)
    lines.append("")
    lines.append(f"Samples evaluated  : {len(y_true_intent)}/{total}")
    if failures:
        lines.append(f"Samples failed     : {len(failures)}")
    lines.append(f"Intent Accuracy    : {intent_acc * 100:.2f}%")
    lines.append(f"Risk Accuracy      : {risk_acc * 100:.2f}%")
    lines.append(f"Priority Accuracy  : {priority_acc * 100:.2f}%")
    lines.append(f"Average Confidence : {avg_confidence:.2f}")
    lines.append("")
    lines.append("Classification Report (Intent)")
    lines.append(report)
    lines.append("")
    lines.append("Confusion Matrix (Intent)")
    lines.append(f"Labels: {intent_labels}")
    lines.append(str(cm))

    if failures:
        lines.append("")
        lines.append("Failures")
        for f in failures:
            lines.append(f"  - {f['subject']}: {f['error']}")

    output = "\n".join(lines)

    print("\n" + output)

    with open("tests/results.txt", "w", encoding="utf-8") as f:
        f.write(output + "\n")

    print("\nResults written to tests/results.txt")


if __name__ == "__main__":
    run_eval()