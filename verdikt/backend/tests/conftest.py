import os
import tempfile
import pytest

# Point the app at an isolated, throwaway SQLite file before anything imports app.database
_tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["VERDIKT_DB_PATH"] = _tmp_db.name


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as c:
        yield c
