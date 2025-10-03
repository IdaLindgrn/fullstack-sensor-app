from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from django.shortcuts import get_object_or_404
from typing import List, Optional
from datetime import datetime
from .models import Sensor
from apps.readings.models import Reading
from .schemas import SensorCreate, SensorUpdate, SensorOut, ReadingCreate, ReadingOut
from .auth import AuthBearer

router = Router()
auth = AuthBearer()


@router.get("/", response=List[SensorOut], auth=auth)
@paginate(PageNumberPagination, page_size=10)
def list_sensors(request, q: Optional[str] = None):
    """List all sensors with optional search by name or model"""
    sensors = Sensor.objects.filter(owner=request.auth)

    if q:
        sensors = sensors.filter(name__icontains=q) | sensors.filter(model__icontains=q)

    # Convert Django models to dictionaries
    return [
        {
            "id": sensor.id,
            "name": sensor.name,
            "model": sensor.model,
            "description": sensor.description,
            "owner_id": sensor.owner.id,
            "created_at": sensor.created_at,
            "updated_at": sensor.updated_at,
        }
        for sensor in sensors
    ]


@router.post("/", response={201: SensorOut}, auth=auth)
def create_sensor(request, data: SensorCreate):
    """Create a new sensor"""
    sensor = Sensor.objects.create(
        owner=request.auth,
        name=data.name,
        model=data.model,
        description=data.description,
    )
    return 201, {
        "id": sensor.id,
        "name": sensor.name,
        "model": sensor.model,
        "description": sensor.description,
        "owner_id": sensor.owner.id,
        "created_at": sensor.created_at,
        "updated_at": sensor.updated_at,
    }


@router.get("/{sensor_id}/", response=SensorOut, auth=auth)
def get_sensor(request, sensor_id: int):
    """Get sensor details"""
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)
    return {
        "id": sensor.id,
        "name": sensor.name,
        "model": sensor.model,
        "description": sensor.description,
        "owner_id": sensor.owner.id,
        "created_at": sensor.created_at,
        "updated_at": sensor.updated_at,
    }


@router.put("/{sensor_id}/", response=SensorOut, auth=auth)
def update_sensor(request, sensor_id: int, data: SensorUpdate):
    """Update sensor"""
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)

    for key, value in data.dict(exclude_unset=True).items():
        setattr(sensor, key, value)

    sensor.save()
    return {
        "id": sensor.id,
        "name": sensor.name,
        "model": sensor.model,
        "description": sensor.description,
        "owner_id": sensor.owner.id,
        "created_at": sensor.created_at,
        "updated_at": sensor.updated_at,
    }


@router.delete("/{sensor_id}/", response={204: None}, auth=auth)
def delete_sensor(request, sensor_id: int):
    """Delete sensor and all its readings"""
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)
    sensor.delete()
    return 204, None


@router.get("/{sensor_id}/readings/", response=List[ReadingOut], auth=auth)
def list_readings(
    request,
    sensor_id: int,
    timestamp_from: Optional[datetime] = None,
    timestamp_to: Optional[datetime] = None,
):
    """List readings for a sensor with optional date range filter"""
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)
    readings = Reading.objects.filter(sensor=sensor)

    if timestamp_from:
        readings = readings.filter(timestamp__gte=timestamp_from)
    if timestamp_to:
        readings = readings.filter(timestamp__lte=timestamp_to)

    return [
        {
            "id": reading.id,
            "sensor_id": reading.sensor.id,
            "temperature": reading.temperature,
            "humidity": reading.humidity,
            "timestamp": reading.timestamp,
            "created_at": reading.created_at,
        }
        for reading in readings
    ]


@router.post("/{sensor_id}/readings/", response={201: ReadingOut}, auth=auth)
def create_reading(request, sensor_id: int, data: ReadingCreate):
    """Create a new reading for a sensor"""
    sensor = get_object_or_404(Sensor, id=sensor_id, owner=request.auth)

    reading = Reading.objects.create(
        sensor=sensor,
        temperature=data.temperature,
        humidity=data.humidity,
        timestamp=data.timestamp,
    )
    return 201, {
        "id": reading.id,
        "sensor_id": reading.sensor.id,
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "timestamp": reading.timestamp,
        "created_at": reading.created_at,
    }
