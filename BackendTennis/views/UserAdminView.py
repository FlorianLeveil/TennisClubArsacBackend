from rest_framework import permissions, generics

from BackendTennis.models import User
from BackendTennis.serializers import UserSerializer


class UserAdminView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
