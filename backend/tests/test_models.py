from app.models.user import User


def test_user_model_tablename() -> None:
    assert User.__tablename__ == "users"