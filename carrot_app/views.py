from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        user = authenticate(username=username, password=password) # will always return the user object.
        login(request, user)
        return HttpResponseRedirect('/')
    return render(request, 'register.html', {});

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
    return render(request, 'login.html', {})

@csrf_exempt
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def index(request):
    if request.user.is_authenticated():
        # render the page that serves logged in home page.
        return render(request, 'base.html', {"user": request.user})
    else:
        # render landing page
        return render(request, 'landing.html', {})
