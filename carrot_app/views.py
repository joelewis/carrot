import json
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from carrot_app.models import *
from carrot_app.utilities import *


from django.conf import settings


@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        user = authenticate(username=username, password=password)   # will always return the user object.
        login(request, user)
        return HttpResponseRedirect('/')
    return render(request, '/', {});

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
    return render(request, '/', {})

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


@login_required
@csrf_exempt
def app_list(request):
    if request.method == 'POST':
        print request.POST
        appname = request.POST['appname']
        if appname == None or appname == '':
            raise Http404
        app = Application(title=appname, user=request.user)
        app.save()
        return HttpResponse(json.dumps(model2dict(app)), content_type="application/json")
    if request.method == 'GET':
        apps = Application.objects.filter(user=request.user)
        response = [model2dict(app) for app in apps]
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
@csrf_exempt
def log_list(request, app_id):
    user = request.user
    if request.method == 'POST':
        data = request.POST
        app = get_object_or_404(Application, id=app_id, user=user)
        print data
        try:
            title = data['title']
            description = data['description']
            link = data.get('link', None)
        except:
            return HttpResponse(status=400)

        log = LogEntry(title=title, description=description, link=link, app=app)
        log.save()
        log_dict = {
        	'title': title,
        	'description': description,
        	'date_created': str(log.date_created),
            'link': link,
        }
        return api_response(log_dict)

    if request.method == 'GET':
        print "request get"
        app = get_object_or_404(Application, id=app_id, user=user)
        logs = [model2dict(logentry) for logentry in LogEntry.objects.filter(app=app)]
        app = model2dict(app)
        host = 'localhost:8000' if settings.LOCAL else settings.HOST
        script_embed = """<script>carrot = {}; carrot.user_identifier='insert unique id of user here'; carrot.app_secret='%s'; </script>\n<script type="text/javascript" src="http://%s/static/js/carrot.js"></script>""" % (app['secret_key'], host)
        app['embed_script'] = script_embed
        app["logs"] = logs
        return api_response(app)
