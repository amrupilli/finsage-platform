from pathlib import Path

from app.ml.scam_detection.train_model import (
    MODEL_PATH,
    EVALUATION_REPORT_PATH,
    build_scam_detection_pipeline,
    train_and_save_model,
)


def test_build_scam_detection_pipeline_has_required_steps() -> None:
    pipeline = build_scam_detection_pipeline()

    assert "tfidf" in pipeline.named_steps
    assert "classifier" in pipeline.named_steps


def test_train_and_save_model_creates_artifact() -> None:
    results = train_and_save_model()
    assert EVALUATION_REPORT_PATH.exists()
    assert Path(results["model_path"]).exists()
    assert MODEL_PATH.exists()
    assert results["train_size"] > 0
    assert results["test_size"] > 0
    assert 0.0 <= results["accuracy"] <= 1.0