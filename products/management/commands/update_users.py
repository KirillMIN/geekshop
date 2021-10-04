from django.core.management.base import BaseCommand

from users.models import User, UserProfileInf


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            user_profile = UserProfileInf.objects.create(user=user)
            user_profile.save()
