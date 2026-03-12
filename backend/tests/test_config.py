from app.core.config import get_settings


def test_settings_load_correctly() -> None:
    settings = get_settings()

    assert settings.app_name == "Finsage Platform API"
    assert settings.app_version == "0.1.0"
    assert settings.debug is True
    assert "finsage_db" in settings.database_url