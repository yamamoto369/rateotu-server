from rest_framework_simplejwt.views import TokenObtainPairView

from rateotu.accounts.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
