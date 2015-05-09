from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        user = request.POST['user']
        passw = request.POST['passw']
        email = request.POST['email']
        user_obj = User.objects.create_user(user, email, passw)
        user_obj.save()
        user_obj = authenticate(user, passw)
        login(request, user_obj)
        return HttpResponseRedirect('/')
    return render(request, 'register.html', {});

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        user = request.POST['user']
        passw = request.POST['passw']
        user_obj = authenticate(user, passw)
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
