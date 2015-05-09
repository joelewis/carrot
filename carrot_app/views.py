from django.http import HttpResponse
from django.shortcuts import render

def user_login(request):
    with open('login.html','r') as file: data=file.readlines()
    return HttpResponse(''.join(data))






def index(request):
    if request.user.is_authenticated():
        # render the page that serves logged in home page.
        pass
    else:
        # render landing page
        return render(request, 'landing.html', {});
