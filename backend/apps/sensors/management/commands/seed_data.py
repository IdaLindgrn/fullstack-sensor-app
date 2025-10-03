from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.sensors.models import Sensor
from apps.readings.models import Reading
from datetime import datetime
import csv
import os

User = get_user_model()


class Command(BaseCommand):
    help = "Load initial sensor data and readings from CSV"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Create user
        user, created = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "username": "admin",
            },
        )
        if created:
            user.set_password("admin123")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user: admin@example.com"))

        # Create sensors
        sensors_data = [
            {"name": "device-001", "model": "EnviroSense"},
            {"name": "device-002", "model": "ClimaTrack"},
            {"name": "device-003", "model": "AeroMonitor"},
            {"name": "device-004", "model": "HydroTherm"},
            {"name": "device-005", "model": "EcoStat"},
        ]

        sensors = {}
        for sensor_data in sensors_data:
            sensor, created = Sensor.objects.get_or_create(
                owner=user,
                name=sensor_data["name"],
                defaults={"model": sensor_data["model"]},
            )
            sensors[sensor_data["name"]] = sensor
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created sensor: {sensor.name}"))

        # Load readings from CSV
        csv_path = "/app/sensor_readings_wide.csv"
        if os.path.exists(csv_path):
            with open(csv_path, "r") as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    # Parse timestamp - handle both formats
                    timestamp_str = row["timestamp"]
                    if "Z" in timestamp_str:
                        timestamp = datetime.fromisoformat(
                            timestamp_str.replace("Z", "+00:00")
                        )
                    else:
                        timestamp = datetime.fromisoformat(timestamp_str)

                    device_id = row["device_id"]

                    # Check if this sensor exists
                    if device_id in sensors:
                        try:
                            Reading.objects.get_or_create(
                                sensor=sensors[device_id],
                                timestamp=timestamp,
                                defaults={
                                    "temperature": float(row["temperature"]),
                                    "humidity": float(row["humidity"]),
                                },
                            )
                            count += 1
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Skipped reading for {device_id}: {e}"
                                )
                            )

                self.stdout.write(self.style.SUCCESS(f"Loaded {count} readings"))
        else:
            self.stdout.write(
                self.style.WARNING("CSV file not found, skipping readings")
            )

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
