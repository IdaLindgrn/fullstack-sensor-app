from ninja.security import HttpBearer
from apps.auth.utils import get_user_from_token


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        user = get_user_from_token(token)
        if user:
            return user
        return None
