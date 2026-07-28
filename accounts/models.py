from django.db import models
from django.contrib.auth.models import User
from common import TimeStampMixin


class Profile(TimeStampMixin):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    is_author = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username