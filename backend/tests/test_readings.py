import pytest
from django.contrib.auth import get_user_model
from apps.sensors.models import Sensor
from apps.readings.models import Reading
from datetime import datetime, timedelta

User = get_user_model()


@pytest.fixture
def sensor(auth_user):
    return Sensor.objects.create(owner=auth_user, name="TestSensor", model="TestModel")


@pytest.mark.django_db
def test_create_reading(client, sensor, auth_token):
    response = client.post(
        f"/sensors/{sensor.id}/readings/",
        json={
            "temperature": 22.5,
            "humidity": 65.0,
            "timestamp": "2024-01-15T10:30:00Z",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 201
    assert response.json()["temperature"] == 22.5


@pytest.mark.django_db
def test_list_readings(client, sensor, auth_token):
    Reading.objects.create(
        sensor=sensor, temperature=20.0, humidity=60.0, timestamp=datetime.now()
    )

    response = client.get(
        f"/sensors/{sensor.id}/readings/",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.django_db
def test_filter_readings_by_date(client, sensor, auth_token):
    now = datetime.now()
    Reading.objects.create(
        sensor=sensor,
        temperature=20.0,
        humidity=60.0,
        timestamp=now - timedelta(days=2),
    )
    Reading.objects.create(
        sensor=sensor, temperature=21.0, humidity=61.0, timestamp=now
    )

    from_date = (now - timedelta(days=1)).isoformat()
    response = client.get(
        f"/sensors/{sensor.id}/readings/?timestamp_from={from_date}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
