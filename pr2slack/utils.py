from django.contrib.auth.models import User
from social_core.backends.utils import user_backends_data
from social_django.utils import BACKENDS, Storage

from slacker import Slacker


def get_slack_client(user):
    backend_data = user_backends_data(user, BACKENDS, Storage)
    user_social_auth = backend_data.get('associated').first()
    access_token = user_social_auth.extra_data.get('access_token')
    return Slacker(access_token)


def get_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None
