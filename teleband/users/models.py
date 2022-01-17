from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from invitations.models import Invitation
import reversion


@reversion.register()
class User(AbstractUser):
    """Default user for TeleBand."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    grade = models.CharField(blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Role(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class GroupInvitation(Invitation):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
