from pathlib import Path

from sklearn import pipeline

import joblib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from app.ml.scam_detection.synthetic_dataset import get_training_texts_and_labels
MODEL_DIR = Path("app/ml/scam_detection/artifacts")
MODEL_PATH = MODEL_DIR / "scam_text_classifier.joblib"
EVALUATION_REPORT_PATH = MODEL_DIR / "scam_model_evaluation.json"


def build_scam_detection_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    ngram_range=(1, 2),
                    min_df=1,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def train_and_save_model() -> dict:
    texts, labels = get_training_texts_and_labels()

    x_train, x_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels,
    )

    pipeline = build_scam_detection_pipeline()
    pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(
        y_test,
        predictions,
        output_dict=True,
        zero_division=0,
    )
    
    evaluation_report = {
    "accuracy": accuracy,
    "classification_report": report,
    "train_size": len(x_train),
    "test_size": len(x_test),
    "model_type": "TF-IDF + Logistic Regression",
    "labels": sorted(set(labels)),
}

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    with EVALUATION_REPORT_PATH.open("w", encoding="utf-8") as file:
        json.dump(evaluation_report, file, indent=2)


    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    return {
    "model_path": str(MODEL_PATH),
    "evaluation_report_path": str(EVALUATION_REPORT_PATH),
    "accuracy": accuracy,
    "classification_report": report,
    "test_size": len(x_test),
    "train_size": len(x_train),
}


if __name__ == "__main__":
    results = train_and_save_model()

    print("Scam detection model trained successfully.")
    print(f"Model saved to: {results['model_path']}")
    print(f"Accuracy: {results['accuracy']:.2f}")
    print(f"Training examples: {results['train_size']}")
    print(f"Test examples: {results['test_size']}")