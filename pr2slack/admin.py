from django.contrib import admin

from pr2slack.models import GithubSecret


admin.site.register(GithubSecret)
