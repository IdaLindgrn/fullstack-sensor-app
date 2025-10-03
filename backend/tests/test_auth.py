import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_success(client):
    response = client.post(
        "/auth/register/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
        },
    )

    assert response.status_code == 200
    assert "token" in response.json()
    assert response.json()["user"]["email"] == "test@example.com"


@pytest.mark.django_db
def test_register_duplicate_email(client):
    User.objects.create_user(
        email="test@example.com", username="existing", password="pass"
    )

    response = client.post(
        "/auth/register/",
        json={
            "email": "test@example.com",
            "username": "newuser",
            "password": "testpass123",
        },
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_success(client):
    user = User.objects.create_user(
        email="test@example.com", username="testuser", password="testpass123"
    )

    response = client.post(
        "/auth/token/", json={"email": "test@example.com", "password": "testpass123"}
    )

    assert response.status_code == 200
    assert "token" in response.json()


@pytest.mark.django_db
def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/token/", json={"email": "wrong@example.com", "password": "wrongpass"}
    )

    assert response.status_code == 401
