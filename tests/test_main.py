from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Application API is running"
    }


def test_register_user():
    import time

    email = f"newtestuser{time.time_ns()}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "name": "New Test User",
            "email": email,
            "password": "Test@123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "New Test User"
    assert data["email"] == email
    assert "password" not in data


def test_duplicate_email():
    response = client.post(
        "/auth/register",
        json={
            "name": "Another User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 409


def test_login():
    response = client.post(
        "/auth/login",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_create_application():
    login_response = client.post(
        "/auth/login",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/applications",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "company": "Amazon",
            "role": "Software Development Engineer",
            "status": "Applied"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "Amazon"
    assert data["role"] == "Software Development Engineer"
    assert data["status"] == "Applied"


def test_get_applications():
    login_response = client.post(
        "/auth/login",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/applications",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_applications():
    login_response = client.post(
        "/auth/login",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/applications?search=Amazon",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    applications = response.json()

    for application in applications:
        assert (
            "amazon" in application["company"].lower()
            or "amazon" in application["role"].lower()
        )


def test_unauthorized_applications():
    response = client.get("/applications")

    assert response.status_code == 401

def test_update_application():
    login_response = client.post(
        "/auth/login",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/applications",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "company": "Google",
            "role": "Software Engineer",
            "status": "Applied"
        }
    )

    assert create_response.status_code == 201

    application_id = create_response.json()["id"]

    update_response = client.put(
        f"/applications/{application_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "status": "Interview"
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == application_id
    assert data["status"] == "Interview"


def test_delete_application():
    login_response = client.post(
        "/auth/login",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/applications",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "company": "Microsoft",
            "role": "Backend Developer",
            "status": "Applied"
        }
    )

    assert create_response.status_code == 201

    application_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/applications/{application_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Application deleted successfully"
    }

    get_response = client.get(
        f"/applications/{application_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert get_response.status_code == 404

def test_create_interview():
    login_response = client.post(
        "/auth/login",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    token = login_response.json()["access_token"]

    application_response = client.post(
        "/applications",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "company": "Microsoft",
            "role": "Software Engineer",
            "status": "Interview"
        }
    )

    assert application_response.status_code == 201

    application_id = application_response.json()["id"]

    interview_response = client.post(
        "/interviews",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "application_id": application_id,
            "interview_date": "2026-11-10T10:00:00",
            "interview_type": "Technical",
            "notes": "DSA and backend interview"
        }
    )

    assert interview_response.status_code == 201

    data = interview_response.json()

    assert data["application_id"] == application_id
    assert data["interview_type"] == "Technical"
    assert data["notes"] == "DSA and backend interview"


def test_get_interviews():
    login_response = client.post(
        "/auth/login",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/interviews",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_specific_interview():
    login_response = client.post(
        "/auth/login",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    token = login_response.json()["access_token"]

    application_response = client.post(
        "/applications",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "company": "Google",
            "role": "Backend Engineer",
            "status": "Interview"
        }
    )

    application_id = application_response.json()["id"]

    interview_response = client.post(
        "/interviews",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "application_id": application_id,
            "interview_date": "2026-11-15T14:00:00",
            "interview_type": "HR",
            "notes": "HR discussion"
        }
    )

    interview_id = interview_response.json()["id"]

    response = client.get(
        f"/interviews/{interview_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == interview_id
    assert data["application_id"] == application_id
    assert data["interview_type"] == "HR"


def test_user_cannot_access_another_users_application():
    # Login as the first user
    user1_login = client.post(
        "/auth/login",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    user1_token = user1_login.json()["access_token"]

    # Create an application for User 1
    application_response = client.post(
        "/applications",
        headers={
            "Authorization": f"Bearer {user1_token}"
        },
        json={
            "company": "Amazon",
            "role": "Software Engineer",
            "status": "Applied"
        }
    )

    assert application_response.status_code == 201

    application_id = application_response.json()["id"]

    # Create User 2
    user2_email = "secondtestuser@example.com"

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Second Test User",
            "email": user2_email,
            "password": "Test@123"
        }
    )

    assert register_response.status_code in [201, 409]

    # Login as User 2
    user2_login = client.post(
        "/auth/login",
        json={
            "name": "Second Test User",
            "email": user2_email,
            "password": "Test@123"
        }
    )

    assert user2_login.status_code == 200

    user2_token = user2_login.json()["access_token"]

    # User 2 tries to access User 1's application
    response = client.get(
        f"/applications/{application_id}",
        headers={
            "Authorization": f"Bearer {user2_token}"
        }
    )

    assert response.status_code == 404