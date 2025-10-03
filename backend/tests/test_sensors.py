import pytest
from django.contrib.auth import get_user_model
from apps.sensors.models import Sensor

User = get_user_model()


@pytest.mark.django_db
def test_create_sensor(client, auth_user, auth_token):
    response = client.post(
        "/sensors/",
        json={
            "name": "Test Sensor",
            "model": "TestModel",
            "description": "A test sensor",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test Sensor"


@pytest.mark.django_db
def test_list_sensors(client, auth_user, auth_token):
    Sensor.objects.create(owner=auth_user, name="Sensor1", model="Model1")
    Sensor.objects.create(owner=auth_user, name="Sensor2", model="Model2")

    response = client.get(
        "/sensors/", headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    assert len(response.json()["items"]) == 2


@pytest.mark.django_db
def test_search_sensors(client, auth_user, auth_token):
    Sensor.objects.create(owner=auth_user, name="device-001", model="EnviroSense")
    Sensor.objects.create(owner=auth_user, name="device-002", model="ClimaTrack")

    response = client.get(
        "/sensors/?q=Enviro", headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    assert len(response.json()["items"]) == 1


@pytest.mark.django_db
def test_delete_sensor(client, auth_user, auth_token):
    sensor = Sensor.objects.create(owner=auth_user, name="ToDelete", model="Model")

    response = client.delete(
        f"/sensors/{sensor.id}/", headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 204
    assert not Sensor.objects.filter(id=sensor.id).exists()


@pytest.mark.django_db
def test_unauthorized_access(client):
    response = client.get("/sensors/")
    assert response.status_code == 401
