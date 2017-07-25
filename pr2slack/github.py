from .utils import *


def pull_request_opened(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_edited(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_closed(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_assigned(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_unassigned(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_synchronize(data):
    pr = data.get('pull_request')


def pull_request_review_requested(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_review_request_removed(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_review_submitted(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_review_edited(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_review_dismissed(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_comment_created(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_comment_edited(channel, repository, data):
    pr = data.get('pull_request')


def pull_request_comment_deleted(channel, repository, data):
    pr = data.get('pull_request')
