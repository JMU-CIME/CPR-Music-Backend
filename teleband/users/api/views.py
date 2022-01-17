import collections
import csv
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from invitations.utils import get_invitation_model
from invitations.exceptions import AlreadyAccepted, AlreadyInvited, UserRegisteredEmail
from invitations.forms import CleanEmailMixin

from .serializers import UserSerializer

User = get_user_model()
Invitation = get_invitation_model()


class IsAdminBulkCreate(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if view.action == "bulk_create":
            return super().has_permission(request, view)
        return True


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = [IsAdminBulkCreate & permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["post"])
    def bulk_create_teachers(self, request):
        users_file = request.FILES["file"]
        contents = "".join([line.decode("utf-8") for line in users_file.readlines()])
        reader = csv.reader(StringIO(contents))

        teacher_group = Group.objects.get(name="Teacher")

        response = collections.defaultdict(list)

        for row in reader:
            # based on https://github.com/bee-keeper/django-invitations/blob/9069002f1a0572ae37ffec21ea72f66345a8276f/invitations/views.py#L63
            invitee = row[0]
            try:
                validate_email(invitee)
                CleanEmailMixin().validate_invitation(invitee)
                invite = Invitation.create(invitee, group=teacher_group)
            except (ValidationError):
                response["invalid"].append({invitee: "invalid email"})
            except (AlreadyAccepted):
                response["invalid"].append({invitee: "already accepted"})
            except (AlreadyInvited):
                response["invalid"].append({invitee: "pending invite"})
            except (UserRegisteredEmail):
                response["invalid"].append({invitee: "user registered email"})
            else:
                invite.send_invitation(request)
                response["valid"].append({invitee: "invited"})

        # created_users = []
        # for row in reader:
        #     created_users.append(
        #         User.objects.create_user(
        #             name=row[0], username=row[1], password=row[2], grade=row[3]
        #         )
        #     )
        #     created_users[-1].groups.add(teacher_group)
        #     created_users[-1].save()

        # serializer = UserSerializer(
        #     created_users, many=True, context={"request": request}
        # )
        return Response(status=status.HTTP_200_OK, data=response)


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
