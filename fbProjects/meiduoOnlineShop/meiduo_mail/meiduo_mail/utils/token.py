from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class Create_token(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # token['name'] = user.name

        return token

    def validate(self, user):
        refresh = self.get_token(user)
        refresh["name"] = user.username
        data = {"user_id": user.id,
                "token": str(refresh.access_token),
                "refresh": str(refresh)}
        return data
