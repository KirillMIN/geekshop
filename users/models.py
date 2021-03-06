from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))
    age = models.PositiveIntegerField(verbose_name='возраст', null=True)

    def is_activation_key_expires(self):
        if now() <= self.activation_key_expires:
            return False
        return True


class UserProfileInf(models.Model):
    male = 'M'
    female = 'W'

    gender_choices = (
        (male, 'м'),
        (female, 'ж'),
    )

    user = models.OneToOneField(
        User,
        unique=True,
        null=False,
        db_index=True,
        on_delete=models.CASCADE
    )

    tagline = models.CharField(verbose_name='тэги', max_length=128, blank=True)

    about_me = models.TextField(verbose_name='о себе', max_length=512, blank=True)

    gender = models.CharField(verbose_name='пол', max_length=1, choices=gender_choices, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfileInf.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofileinf.save()
