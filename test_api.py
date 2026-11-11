import pytest
import jwt
import datetime
from finance_server import app, hash_password, SECRET_KEY

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_password_hashing():
    hashed = hash_password("mysecret123")
    assert hashed != "mysecret123"
    assert len(hashed) == 64  # SHA-256 produces a 64-character hex string

def test_unauthorized_ledger_access_blocked(client):
    # Try accessing /ledger without a JWT wristband
    response = client.get("/ledger")
    assert response.status_code == 401
    assert b"Missing or invalid security token" in response.data

def test_tampered_jwt_token_rejected(client):
    # Try sneaking past the bouncer with a fake token
    headers = {"Authorization": "Bearer fake.tampered.token"}
    response = client.get("/ledger", headers=headers)
    assert response.status_code == 401
    assert b"Tampered or invalid token" in response.data
