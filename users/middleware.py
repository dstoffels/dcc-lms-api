class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        bypass_paths = ["auth/login", "auth/register"]
        path = request.path_info.lstrip("/")

        if path not in bypass_paths:
            token = request.COOKIES.get("access_token")
            if token:
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        response = self.get_response(request)
        return response
