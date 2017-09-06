from django.contrib.auth.models import User
from social_core.backends.utils import user_backends_data
from social_django.utils import BACKENDS, Storage

from slacker import Slacker

from pr2slack.models import PullReqeustThread


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


def get_slack_username(user):
    if isinstance(user, str):
        user = get_user(user)

    if user is None:
        return None

    backend_data = user_backends_data(user, BACKENDS, Storage)
    user_social_auth = backend_data.get('associated').first()
    return '<@{}>'.format(user_social_auth.uid)


def message_with_mention(message, user):
    username = get_slack_username(user)
    return '{} {}'.format(username, message) if username else message


def post_message(channel, repository, data, message):
    pr = data.get('pull_request')
    thread_ts = PullReqeustThread.objects.get(
        repository=repository,
        pull_request=pr.get('number'),
    ).thread

    sender = data.get('sender').get('login')
    mention = data.get('user').get('login')
    if sender == mention:
        return

    user = User.objects.get(username=sender)
    slack = get_slack_client(user)
    slack.chat.post_message(channel,
                            text=message_with_mention(message, mention),
                            thread_ts=thread_ts,
                            as_user=True
                            )