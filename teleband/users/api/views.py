from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class IsAuthForDelete(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == "DELETE":
            return super().has_permission(request, view)
        return True


class ObtainDeleteAuthToken(ObtainAuthToken):
    permission_classes = [IsAuthForDelete]

    def delete(self, request, *args, **kwargs):
        try:
            Token.objects.get(user=request.user).delete()
            return Response(status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


obtain_delete_auth_token = ObtainDeleteAuthToken.as_view()
