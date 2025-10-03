import pytest
from django.contrib.auth import get_user_model
from ninja.testing import TestClient
from ninja import NinjaAPI
from apps.auth.api import router as auth_router
from apps.sensors.api import router as sensors_router
from apps.auth.utils import create_token

User = get_user_model()

test_api = NinjaAPI(
    title="Test Sensor Readings API", version="1.0.0", urls_namespace="testapi"
)
test_api.add_router("/auth/", auth_router, tags=["Authentication"])
test_api.add_router("/sensors/", sensors_router, tags=["Sensors"])


@pytest.fixture(scope="session")
def client():
    return TestClient(test_api)


@pytest.fixture
@pytest.mark.django_db
def auth_user():
    user = User.objects.create_user(
        email="test@example.com", username="testuser", password="pass"
    )
    return user


@pytest.fixture
def auth_token(auth_user):
    return create_token(auth_user.id)
