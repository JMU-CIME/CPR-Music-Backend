import logging

from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from invitations.signals import invite_accepted
from invitations.utils import get_invitation_model

logger = logging.getLogger(__name__)


def handle_invite_accepted(sender, email, **kwargs):
    try:
        User = get_user_model()
        Invitation = get_invitation_model()

        user = User.objects.get(email=email)
        group = Invitation.objects.get(email=email).group
        user.groups.add(group)
    except User.DoesNotExist:
        logger.error(
            "Handling invite accepted signal for {} but no such user".format(email)
        )
    except Invitation.DoesNotExist:
        logger.error(
            "Handling invite accepted signal for {} but no such invitation".format(
                email
            )
        )


class UsersConfig(AppConfig):
    name = "teleband.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import teleband.users.signals  # noqa F401
        except ImportError:
            pass

        invite_accepted.connect(handle_invite_accepted)
