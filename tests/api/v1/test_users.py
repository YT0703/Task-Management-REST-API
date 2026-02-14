# tests/api/v1/test_users.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.user import UserCreate


def test_create_user(client: TestClient) -> None:
    data = {"email": "test@example.com", "password": "password123"}
    r = client.post(f"{settings.API_V1_STR}/users/", json=data)
    assert r.status_code == 201
    created_user = r.json()
    assert created_user["email"] == data["email"]
    assert "id" in created_user
    assert "is_active" in created_user


def test_create_existing_user(client: TestClient) -> None:
    data = {"email": "test@example.com", "password": "password123"}
    client.post(f"{settings.API_V1_STR}/users/", json=data)
    r = client.post(f"{settings.API_V1_STR}/users/", json=data)
    assert r.status_code == 400
    assert r.json()["detail"] == "The user with this username already exists in the system."


def test_login_for_access_token(client: TestClient) -> None:
    # ユーザー登録
    user_data = {"email": "login_test@example.com", "password": "password123"}
    client.post(f"{settings.API_V1_STR}/users/", json=user_data)

    # ログイン
    login_data = {"username": "login_test@example.com", "password": "password123"}
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data
    )
    assert r.status_code == 200
    token_data = r.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient) -> None:
    user_data = {"email": "wrong_password_test@example.com", "password": "password123"}
    client.post(f"{settings.API_V1_STR}/users/", json=user_data)

    login_data = {"username": "wrong_password_test@example.com", "password": "wrong_password"}
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Incorrect username or password"


def test_read_users_me(client: TestClient) -> None:
    # ユーザー登録
    user_data = {"email": "me_test@example.com", "password": "password123"}
    client.post(f"{settings.API_V1_STR}/users/", json=user_data)

    # ログインしてトークン取得
    login_data = {"username": "me_test@example.com", "password": "password123"}
    login_r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data
    )
    token = login_r.json()["access_token"]

    # 認証済みユーザー情報取得
    r = client.get(
        f"{settings.API_V1_STR}/users/me/", headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200
    current_user = r.json()
    assert current_user["email"] == user_data["email"]
    assert "id" in current_user


def test_read_users_me_unauthorized(client: TestClient) -> None:
    # 認証なしでアクセス
    r = client.get(f"{settings.API_V1_STR}/users/me/")
    assert r.status_code == 401
    assert r.json()["detail"] == "Not authenticated"



