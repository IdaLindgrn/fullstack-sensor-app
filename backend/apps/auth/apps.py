from django.apps import AppConfig


class CustomAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.auth"
    label = "custom_auth"  # This gives it a unique label to avoid conflict with django.contrib.auth
