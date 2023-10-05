import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_auth_logout
from urllib.parse import urlencode
from django.conf import settings

def login(request):
  return render(request, 'login.html')

@login_required
def home(request):
  return render(request, 'home.html')

def logout(request):
    django_auth_logout(request)
    return_to = urlencode({'redirect_uri': request.build_absolute_uri('http://localhost:8000/')})
    logout_url = 'https://%s/auth-ui/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AIC_DOMAIN, settings.SOCIAL_AUTH_AIC_KEY, return_to)
    return redirect(logout_url)

@login_required
def dashboard(request):
    user = request.user
    aicuser = user.social_auth.get(provider='aic')
    userdata = {
        'user_id': aicuser.uid,
        'name': user.first_name,
        'lname': user.last_name,
        'issuer': aicuser.extra_data['iss'],
        'email': user.email,
        'access_token': aicuser.extra_data['access_token'],
        'picture': None,
        'auth_time': aicuser.extra_data['auth_time'],
        'token_type':aicuser.extra_data['token_type']
    }

    return render(request, 'dashboard.html', {
        'userdata': json.dumps(userdata, indent=4)
    })