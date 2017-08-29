from django.contrib import admin

from pr2slack.models import GithubSecret, PullReqeustThread

admin.site.register(PullReqeustThread)
admin.site.register(GithubSecret)
