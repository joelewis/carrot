from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import models, authenticate, login

def user_signup(request):
    if request.method == 'POST':
        user = request.POST['user']; passw = request.POST['passw']
        email = request.POST['email']
        user_obj = models.User.objects.create_user(user, email, passw)
        user_obj.save()
        login(request, user_obj)
        return HttpResponseRedirect('/')
    return render(request, 'register.html', {});

def user_login(request):
    if request.method == 'POST':
        user = request.POST['user']; passw = request.POST['passw']
        user_obj = authenticate(user,passw)
        if user is not None:
            login(request, user_obj)
            return HttpResponseRedirect('/')
    return render(request, 'login.html', {})

def index(request):
    if request.user.is_authenticated():
        # render the page that serves logged in home page.
        pass
    else:
        # render landing page
        return render(request, 'landing.html', {})
