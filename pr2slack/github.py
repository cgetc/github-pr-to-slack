from .models import PullReqeustThread
from .utils import *


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


# def pull_request_edited(channel, repository, data):
#     pr = data.get('pull_request')


def pull_request_closed(channel, repository, data):
    pr = data.get('pull_request')
    thread_ts = PullReqeustThread.objects.get(
        repository=repository,
        pull_request=pr.get('number'),
    ).thread
    reviewer = get_slack_username(pr.get('assignee').get('login'))

    username = pr.get('user').get('login')
    user = User.objects.get(username=username)
    slack = get_slack_client(user)
    slack.chat.post_message(channel,
                            text='{} マージしました。'.format(reviewer),
                            thread_ts=thread_ts,
                            as_user=True
                            )


def pull_request_assigned(channel, repository, data):
    pr = data.get('pull_request')
    thread_ts = PullReqeustThread.objects.get(
        repository=repository,
        pull_request=pr.get('number'),
    ).thread

    reviewer = data.get('assignee').get('login')
    username = pr.get('user').get('login')
    if reviewer == username:
        return
    else:
        reviewer = get_slack_username(reviewer)

    user = User.objects.get(username=username)
    slack = get_slack_client(user)
    slack.chat.post_message(channel,
                            text='{} レビューお願いします。'.format(reviewer),
                            thread_ts=thread_ts,
                            as_user=True
                            )


def pull_request_unassigned(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_synchronize(data):
    pr = data.get('pull_request')


# def pull_request_review_requested(channel, repository, data):
#     pr = data.get('pull_request')
#
#
# def pull_request_review_request_removed(channel, repository, data):
#     pr = data.get('pull_request')


def pull_request_review_submitted(channel, repository, data):
    pr = data.get('pull_request')


# def pull_request_review_edited(channel, repository, data):
#     pr = data.get('pull_request')
#
#
# def pull_request_review_dismissed(channel, repository, data):
#     pr = data.get('pull_request')
#
#
# def pull_request_comment_created(channel, repository, data):
#     pr = data.get('pull_request')
#
#
# def pull_request_comment_edited(channel, repository, data):
#     pr = data.get('pull_request')
#
#
# def pull_request_comment_deleted(channel, repository, data):
#     pr = data.get('pull_request')
