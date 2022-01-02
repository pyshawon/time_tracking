from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def create_auth_token(sender, instance, created, **kwargs):
    """
    Post save signal for create TOKEN for User.
    """
    if created:
        Token.objects.create(user=instance)


post_save.connect(create_auth_token, User)
