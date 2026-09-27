import pytest

pytest_plugins = ["pytest_homeassistant_custom_component"]


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


@pytest.fixture(autouse=True)
def german_home_assistant(hass, request):
    """Die Tests gehen von einem deutschen Home Assistant aus (Start-Kategorien usw. auf Deutsch)."""
    if "english" not in request.keywords:
        hass.config.language = "de"
    yield


def pytest_configure(config):
    config.addinivalue_line("markers", "english: Home Assistant läuft auf Englisch")
