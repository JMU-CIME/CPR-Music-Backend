from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

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


# class ObtainDeleteAuthToken(ObtainAuthToken)
#     permission_classes = [IsAuthForDelete]

#     def delete(self, request, *args, **kwargs):
#         try:
#             Token.objects.get(key=request.data).delete()
#             return Response(status=status.HTTP_200_OK)
#         except Token.DoesNotExist:
#             logger.info("idk y'all")
#             return Response(status=status.HTTP_404_NOT_FOUND)
