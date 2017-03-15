# -*- coding: utf8 -*-

"Login views"

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    "Login view"
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def logout_user(request):
    "Logout view"
    logout(request)
    return JsonResponse({'success': True})
