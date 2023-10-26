from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from .cookies import set_cookies, set_new_cookies
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny


class LoginView(TokenObtainPairView):
    """CustomTokenObtainPairView overrides the default TokenObtainPairView to add cookie
    handling for access and refresh tokens. The post method is overridden to set the
    access and refresh tokens as cookies in the response if token=true is passed.
    The response data is also cleared if token=false."""

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return set_cookies(request, response)


class RefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        if "refresh" not in request.data:
            token = request.COOKIES.get("refresh_token")
            if token:
                request.data["refresh"] = token
        response = super().post(request, *args, **kwargs)

        return set_cookies(request, response)


User = get_user_model()


class RegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            return set_new_cookies(request, response)

        return response
