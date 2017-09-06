# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from .models import PullReqeustThread
from .utils import get_slack_client, message_with_mention, post_message


def pull_request_opened(channel, repository, data):
    pr = data.get('pull_request')

    username = pr.get('user').get('login')
    user = User.objects.get(username=username)
    slack = get_slack_client(user)
    response = slack.chat.post_message(
        channel, text='{title}\n{html_url}'.format(**pr), as_user=True)

    PullReqeustThread.objects.create(
        channel=channel,
        thread=response.body.get('ts'),
        repository=repository,
        pull_request=pr.get('number')
    )


def pull_request_edited(channel, repository, data):
    post_message(channel, repository, data, '更新しました。')


def pull_request_closed(channel, repository, data):
    pass


def pull_request_assigned(channel, repository, data):
    pr = data.get('pull_request')
    thread_ts = PullReqeustThread.objects.get(
        repository=repository,
        pull_request=pr.get('number'),
    ).thread

    reviewer = data.get('assignee').get('login')
    username = data.get('sender').get('login')
    if reviewer == username:
        return

    user = User.objects.get(username=username)
    slack = get_slack_client(user)
    slack.chat.post_message(channel,
                            text=message_with_mention('レビューお願いします。', reviewer),
                            thread_ts=thread_ts,
                            as_user=True
                            )


def pull_request_unassigned(channel, repository, data):
    post_message(channel, repository, data, 'レビューワーから外れました。')


def pull_request_synchronize(channel, repository, data):
    post_message(channel, repository, data, 'synchronized.')


def pull_request_review_requested(channel, repository, data):
    post_message(channel, repository, data, 'review_requested.')


def pull_request_review_request_removed(channel, repository, data):
    post_message(channel, repository, data, 'review_request_removed.')


def pull_request_review_submitted(channel, repository, data):
    post_message(channel, repository, data, 'review_submitted.')


def pull_request_review_edited(channel, repository, data):
    post_message(channel, repository, data, 'review_edited.')


def pull_request_review_dismissed(channel, repository, data):
    post_message(channel, repository, data, 'review_dismissed.')


def pull_request_comment_created(channel, repository, data):
    post_message(channel, repository, data, 'comment_created.')


def pull_request_comment_edited(channel, repository, data):
    post_message(channel, repository, data, 'comment_edited.')


def pull_request_comment_deleted(channel, repository, data):
    post_message(channel, repository, data, 'comment_deleted.')
