# tests/test_smoke.py
import io
import json
import pandas as pd
from src.app import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_health(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    d = rv.get_json()
    assert d["status"] == "ok"

def test_upload_and_summary(client, tmp_path):
    # create a small CSV
    df = pd.DataFrame({"a":[1,2,3],"b":[4,5,6]})
    p = tmp_path / "small.csv"
    df.to_csv(p, index=False)
    with open(p, "rb") as f:
        rv = client.post("/upload", data={"file": (f, "small.csv")})
    assert rv.status_code == 200
    j = rv.get_json()
    assert j["rows"] == 3
    # summary
    rv2 = client.get("/summary")
    assert rv2.status_code == 200
    summary = rv2.get_json()
    assert "a" in summary
    assert "mean" in summary["a"]

