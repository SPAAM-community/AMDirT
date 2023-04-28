from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Path to test data directory"""
    return Path(__file__).parent / "data"
