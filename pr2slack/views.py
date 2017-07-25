from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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
