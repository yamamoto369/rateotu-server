from rest_framework_simplejwt.views import TokenObtainPairView

from rateotu.accounts.serializers import CustomJwtTokenObtainPairSerializer


class CustomJwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomJwtTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
