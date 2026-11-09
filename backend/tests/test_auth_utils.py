from uuid import uuid4

import jwt

from app.core import security


PASSWORD = "TestPassword123!"
JWT_SECRET_KEY = "test-secret-key-for-unit-tests-2026"

def test_password_hash_and_verify():
    password = PASSWORD

    hashed_password = security.get_password_hash(password)

    assert hashed_password != password
    assert security.verify_password(password, hashed_password)


def test_password_verify_rejects_wrong_password():
    password = PASSWORD

    hashed_password = security.get_password_hash(password)

    assert not security.verify_password(
        "WrongPassword123!",
        hashed_password,
    )


def test_create_and_decode_access_token(monkeypatch):
    monkeypatch.setattr(
        security,
        "JWT_SECRET_KEY",
        JWT_SECRET_KEY,
    )

    user_id = uuid4()

    token = security.create_access_token(user_id)
    decoded_user_id = security.decode_access_token(token)

    assert decoded_user_id == user_id


def test_decode_invalid_access_token(monkeypatch):
    monkeypatch.setattr(
        security,
        "JWT_SECRET_KEY",
        JWT_SECRET_KEY,
    )

    try:
        security.decode_access_token("invalid-token")
        assert False, "Expected an invalid token exception"
    except jwt.InvalidTokenError:
        pass