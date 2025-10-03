from django.db import models
from apps.sensors.models import Sensor


class Reading(models.Model):
    sensor = models.ForeignKey(
        Sensor, on_delete=models.CASCADE, related_name="readings"
    )
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["sensor", "timestamp"]),
        ]
        unique_together = [["sensor", "timestamp"]]

    def __str__(self):
        return f"{self.sensor.name} - {self.timestamp}"
