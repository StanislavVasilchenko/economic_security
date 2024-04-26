from django.core.management import BaseCommand

from users.models import User
from private_keys import S_USER_EMAIL, S_USER_PASSWORD, S_USER_FIRST_NAME, S_USER_LAST_NAME


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.create(
            email=S_USER_EMAIL,
            first_name=S_USER_FIRST_NAME,
            last_name=S_USER_LAST_NAME,
            is_staff=True,
            is_superuser=True,
        )

        users.set_password(S_USER_PASSWORD)
        users.save()
