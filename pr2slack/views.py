import hashlib
import hmac
import json

from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from pr2slack import github
from pr2slack.forms import ProfileForm


def index(req):
    return render(req, 'index.html', {})


def logout(req):
    # Call django's standard logout view
    auth_logout(req)
    return redirect('index')


@login_required
def update_profile(req):
    if req.method == 'POST':
        form = ProfileForm(req.POST)
        if form.is_valid():
            user = req.user
            user.username = form.cleaned_data['username']
            user.save()
    else:
        form = ProfileForm(initial={
            'username': req.user.username
        })

    return render(req, 'accounts/profile.html', {
        'form': form,
    })


@csrf_exempt
def github_hooks(req, channel):
    if req.method != 'POST':
        return HttpResponseBadRequest(req)

    data = json.loads(req.body.decode('utf8'))
    repository = data.get('repository').get('name')
    try:
        secret = settings.GITHUB_REPO_SECRETS[repository]
    except KeyError:
        return HttpResponseNotFound(req)

    signature = hmac.new(secret, req.body, hashlib.sha1).hexdigest()
    if signature != req.META['HTTP_X_HUB_SIGNATURE'][5:]:
        return HttpResponseForbidden(req)

    event = req.META['HTTP_X_GITHUB_EVENT']
    action = data.get('action')
    try:
        handler = getattr(github, '{}_{}'.format(event, action) if action else event)
    except AttributeError:
        pass
    else:
        if callable(handler):
            handler(channel, repository, data)

    return HttpResponse(req, '', status=204)
