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

stuff = ''' <div style="text-shadow: none" class="alert alert-danger alert-dismissible fade in" role="alert">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4>Oh snap! %s failed!</h4>
                <p> %s </p></div>
                <script> $('#myModal a[href="#%s"]').tab('show') </script>
                <script> $('#myModal').modal('show') </script>'''

@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except Exception:
            do = 'Signup'
            what = "Username already exists! Please choose a different name."
            return render(request, 'landing.html', {'login_fail': '', 'signup_fail': stuff % ('Signup', what, 'signup')})
        user.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect('/')

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
    what = "Please ensure that you've given the correct login credentials."
    return render(request, 'landing.html', {'signup_fail': '', 'login_fail': stuff % ('Login', what, 'login')})

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
        return render(request, 'landing.html', {'login_fail': '', 'signup_fail': ''})

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
def log_kill(request, app_id, log_id):
    user = request.user
    if request.method == 'DELETE':
        app = get_object_or_404(Application, id=app_id, user=user)
        LogEntry.objects.get(id=log_id).delete()
        return HttpResponse(json.dumps({'success':True}), content_type="application/json")

@login_required
@csrf_exempt
def app_kill(request, app_id):
    user = request.user
    if request.method == 'DELETE':
        app = get_object_or_404(Application, id=app_id, user=user)
        LogEntry.objects.filter(app=app).delete()
        LogEntryRead.objects.filter(app=app).delete()
        Application.objects.get(id=app_id).delete()
        return HttpResponse(json.dumps({'success':True}), content_type="application/json")

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

    elif request.method == 'GET':
        print "request get"
        app = get_object_or_404(Application, id=app_id, user=user)
        logs = [model2dict(logentry) for logentry in LogEntry.objects.filter(app=app)]
        app = model2dict(app)
        host = 'localhost:8000' if settings.LOCAL else settings.HOST
        script_embed = """<script>carrot = {}; carrot.user_identifier='insert unique id of user here'; carrot.app_secret='%s'; </script>\n<script type="text/javascript" src="http://%s/static/js/carrot.js"></script>""" % (app['secret_key'], host)
        app['embed_script'] = script_embed
        app["logs"] = logs
        return api_response(app)

# carrot.js related views

def get_unread_logentry_list(app, user_id):
	"""
	returns a list of log entries for <app> that are unread by the given <user_id>
	"""
	read_logentries = [logentryread.log for logentryread in LogEntryRead.objects.filter(app=app, user_id=user_id)]
	unreads = [entry for entry in LogEntry.objects.filter(app=app) if entry not in read_logentries]
	return unreads

def unread_count(request, app_key, user_id):
    app = Application.objects.get(secret_key=app_key)
    count = len(get_unread_logentry_list(app, user_id))
    if request.GET.get('callback') != None:
    	return HttpResponse(request.GET.get('callback') + '({ count: %s})' % count, content_type="application/json")
    return HttpResponse(str(count))

def unread_logs(request, app_key, user_id):
	"""
	returns a jsonp or json formatted unread notifications(log entries)
	"""
	app = Application.objects.get(secret_key=app_key)
	notifications = [model2dict(e) for e in get_unread_logentry_list(app, user_id)]
	if request.GET.get('callback') != None:
		return HttpResponse(request.GET.get('callback') + '({ data: ' + json.dumps(notifications, indent=4) + '})', content_type="application/json")
	else:
		return HttpResponse(json.dumps(notifications, indent=4), content_type="application/json")

def mark_as_read(request, app_key, user_id):
	"""
	mark all unread notifications for that user, as read
	"""
	app = Application.objects.get(secret_key=app_key)
	unreads = get_unread_logentry_list(app, user_id)
	for log in unreads:
		logentryread = LogEntryRead(app=app, log=log, user_id=user_id)
		logentryread.save()
	message = 'marked {0} notifications as read'.format(len(unreads))
	if request.GET.get('callback') != None:
		return HttpResponse(request.GET.get('callback') + '({ "message": "' + message + '"})', content_type="application/json")
	else:
		return HttpResponse(json.dumps({'message':message}, indent=4), content_type="application/json")

def render_iframe(request, app_key, user_id):
	app = Application.objects.get(secret_key=app_key)
	notifications = [model2dict(e) for e in get_unread_logentry_list(app, user_id)]
	response = render(request, 'notification_frame.html', dict(notifications=notifications))
	response['X-Frame-Options'] = 'ALLOWALL'
	return response
