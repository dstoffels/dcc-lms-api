from rest_framework.response import Response
from rest_framework.request import Request
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


def set_cookies(request: Request, response: Response):
    access_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
    refresh_lifetime = settings.SIMPLE_JWT["SLIDING_TOKEN_REFRESH_LIFETIME"].total_seconds()

    response.set_cookie(
        "access_token", response.data["access"], httponly=True, max_age=access_lifetime, secure=settings.HTTPS_ONLY
    )
    response.set_cookie(
        "refresh_token", response.data["refresh"], httponly=True, max_age=refresh_lifetime, secure=settings.HTTPS_ONLY
    )

    use_jwt_in_response = request.GET.get("token", "false").lower() == "true"

    if not use_jwt_in_response:
        response.data = {}

    return response


def set_new_cookies(request: Request, response: Response):
    access_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
    refresh_lifetime = settings.SIMPLE_JWT["SLIDING_TOKEN_REFRESH_LIFETIME"].total_seconds()

    refresh = RefreshToken.for_user(response.data.serializer.context.get("user"))
    access = str(refresh.access_token)
    refresh = str(refresh)

    response.set_cookie("access_token", access, httponly=True, max_age=access_lifetime, secure=settings.HTTPS_ONLY)
    response.set_cookie("refresh_token", refresh, httponly=True, max_age=refresh_lifetime, secure=settings.HTTPS_ONLY)
    use_token = request.GET.get("token", "false").lower() == "true"
    if use_token:
        response.data.update({"access": access, "refresh": refresh})
    return response
