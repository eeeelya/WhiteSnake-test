from core.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user: User) -> str:
    refresh = RefreshToken.for_user(user)

    return f"Whitesnake {refresh.access_token}"
