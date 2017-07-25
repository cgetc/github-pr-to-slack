from django.db import models


class PullReqeustThread(models.Model):
    channel = models.TextField()
    thread = models.TextField()
    repository = models.TextField()
    pull_request = models.TextField()

    class Meta:
        db_table = 'p2t_pull_reqeust_thread'
        unique_together = (
            ('channel', 'thread'),
            ('repository', 'pull_request'),
        )
