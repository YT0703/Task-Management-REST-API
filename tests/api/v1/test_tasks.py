# tests/api/v1/test_tasks.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.user import UserCreate


def get_authenticated_user_token(client: TestClient, email: str, password: str) -> str:
    # ユーザー登録
    user_data = {"email": email, "password": password}
    client.post(f"{settings.API_V1_STR}/users/", json=user_data)

    # ログインしてトークン取得
    login_data = {"username": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data
    )
    return r.json()["access_token"]


def test_create_task(client: TestClient) -> None:
    token = get_authenticated_user_token(client, "task_owner@example.com", "password123")
    
    task_data = {"title": "Test Task", "description": "This is a test task."}
    r = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json=task_data,
    )
    assert r.status_code == 201
    created_task = r.json()
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]
    assert "id" in created_task
    assert "owner_id" in created_task
    assert created_task["completed"] is False


def test_create_task_unauthorized(client: TestClient) -> None:
    task_data = {"title": "Unauthorized Task", "description": "Should fail."}
    r = client.post(
        f"{settings.API_V1_STR}/tasks/",
        json=task_data,
    )
    assert r.status_code == 401
    assert r.json()["detail"] == "Not authenticated"


def test_read_user_tasks(client: TestClient) -> None:
    email = "read_tasks_owner@example.com"
    token = get_authenticated_user_token(client, email, "password123")

    # タスクをいくつか作成
    client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Task 1", "description": "Desc 1"},
    )
    client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Task 2", "description": "Desc 2"},
    )

    r = client.get(
        f"{settings.API_V1_STR}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    tasks = r.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 1"
    assert tasks[1]["title"] == "Task 2"


def test_read_task_by_id(client: TestClient) -> None:
    email = "read_single_task_owner@example.com"
    token = get_authenticated_user_token(client, email, "password123")

    # タスク作成
    task_data = {"title": "Single Task", "description": "Detail for single task."}
    create_r = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json=task_data,
    )
    task_id = create_r.json()["id"]

    # IDでタスク取得
    r = client.get(
        f"{settings.API_V1_STR}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    task = r.json()
    assert task["id"] == task_id
    assert task["title"] == task_data["title"]


def test_read_task_by_id_not_found(client: TestClient) -> None:
    email = "read_not_found_owner@example.com"
    token = get_authenticated_user_token(client, email, "password123")

    r = client.get(
        f"{settings.API_V1_STR}/tasks/9999",  # 存在しないID
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"


def test_read_task_by_id_forbidden(client: TestClient) -> None:
    # ユーザー1がタスクを作成
    email1 = "owner1@example.com"
    token1 = get_authenticated_user_token(client, email1, "password123")
    task_data = {"title": "Owner1's Task", "description": "This is owner1's task."}
    create_r = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers={"Authorization": f"Bearer {token1}"},
        json=task_data,
    )
    task_id = create_r.json()["id"]

    # ユーザー2が同じタスクにアクセスしようとする
    email2 = "owner2@example.com"
    token2 = get_authenticated_user_token(client, email2, "another_password")
    r = client.get(
        f"{settings.API_V1_STR}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Not authorized to access this task"


def test_update_task(client: TestClient) -> None:
    email = "update_task_owner@example.com"
    token = get_authenticated_user_token(client, email, "password123")

    # タスク作成
    initial_task_data = {"title": "Old Title", "description": "Old Description"}
    create_r = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json=initial_task_data,
    )
    task_id = create_r.json()["id"]

    # タスク更新
    update_task_data = {"title": "New Title", "description": "New Description", "completed": True}
    r = client.put(
        f"{settings.API_V1_STR}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_task_data,
    )
    assert r.status_code == 200
    updated_task = r.json()
    assert updated_task["id"] == task_id
    assert updated_task["title"] == update_task_data["title"]
    assert updated_task["description"] == update_task_data["description"]
    assert updated_task["completed"] is True


def test_update_task_forbidden(client: TestClient) -> None:
    # ユーザー1がタスクを作成
    email1 = "update_owner1@example.com"
    token1 = get_authenticated_user_token(client, email1, "password123")
    task_data = {"title": "Owner1's Task", "description": "This is owner1's task."}
    create_r = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers={"Authorization": f"Bearer {token1}"},
        json=task_data,
    )
    task_id = create_r.json()["id"]

    # ユーザー2が同じタスクを更新しようとする
    email2 = "update_owner2@example.com"
    token2 = get_authenticated_user_token(client, email2, "another_password")
    update_task_data = {"title": "Unauthorized Update", "description": "Should fail.", "completed": True}
    r = client.put(
        f"{settings.API_V1_STR}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token2}"},
        json=update_task_data,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Not authorized to update this task"


def test_delete_task(client: TestClient) -> None:
    email = "delete_task_owner@example.com"
    token = get_authenticated_user_token(client, email, "password123")

    # タスク作成
    task_data = {"title": "Task to Delete", "description": "This task will be deleted."}
    create_r = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json=task_data,
    )
    task_id = create_r.json()["id"]

    # タスク削除
    r = client.delete(
        f"{settings.API_V1_STR}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    deleted_task = r.json()
    assert deleted_task["id"] == task_id

    # 削除されたことを確認（404が返るはず）
    r = client.get(
        f"{settings.API_V1_STR}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404


def test_delete_task_forbidden(client: TestClient) -> None:
    # ユーザー1がタスクを作成
    email1 = "delete_owner1@example.com"
    token1 = get_authenticated_user_token(client, email1, "password123")
    task_data = {"title": "Owner1's Task", "description": "This is owner1's task."}
    create_r = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers={"Authorization": f"Bearer {token1}"},
        json=task_data,
    )
    task_id = create_r.json()["id"]

    # ユーザー2が同じタスクを削除しようとする
    email2 = "delete_owner2@example.com"
    token2 = get_authenticated_user_token(client, email2, "another_password")
    r = client.delete(
        f"{settings.API_V1_STR}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Not authorized to delete this task"



