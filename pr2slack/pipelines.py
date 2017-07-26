from django.shortcuts import redirect


def extra_scope(backend, details, response, *args, **kwargs):
    if 'chat:write:user' not in response.get('scope'):
        backend.get_scope = lambda: ['chat:write:user']
        auth_url = backend.auth_url()
        return redirect(auth_url)
