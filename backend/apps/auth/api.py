from ninja import Router
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from .schemas import RegisterSchema, LoginSchema, TokenResponse, UserOut, ErrorResponse
from .utils import create_token

router = Router()
User = get_user_model()


@router.post("/register/", response={200: TokenResponse, 400: ErrorResponse})
def register(request, data: RegisterSchema):
    """Register a new user and return authentication token"""
    if User.objects.filter(email=data.email).exists():
        return 400, {"detail": "Email already registered"}

    if User.objects.filter(username=data.username).exists():
        return 400, {"detail": "Username already taken"}

    user = User.objects.create(
        email=data.email, username=data.username, password=make_password(data.password)
    )

    token = create_token(user.id)

    return {
        "token": token,
        "user": UserOut(id=user.id, email=user.email, username=user.username),
    }


@router.post("/token/", response={200: TokenResponse, 401: ErrorResponse})
def login(request, data: LoginSchema):
    """Login with email and password to get authentication token"""
    try:
        user = User.objects.get(email=data.email)
    except User.DoesNotExist:
        return 401, {"detail": "Invalid credentials"}

    if not check_password(data.password, user.password):
        return 401, {"detail": "Invalid credentials"}

    token = create_token(user.id)

    return {
        "token": token,
        "user": UserOut(id=user.id, email=user.email, username=user.username),
    }
