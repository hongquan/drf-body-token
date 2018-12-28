
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from drf_body_token.authentication import BodyTokenAuthentication


User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [BodyTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
