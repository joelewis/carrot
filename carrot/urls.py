"""carrot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from carrot_app import views

urlpatterns = [
    url(r'^login/$', views.user_login),
    url(r'^signup/$', views.user_signup),
    url(r'^logout/$', views.user_logout),
    url(r'^$', views.index),
    url(r'^apps/.*?', views.index),
    url(r'^api/v1/apps$', views.app_list),
    url(r'^api/v1/apps/(?P<app_id>\d+)$', views.log_list),
    url(r'^api/v1/apps/delete/(?P<app_id>\d+)$', views.app_kill),
    url(r'^api/v1/apps/(?P<app_id>\d+)/(?P<log_id>\d+)$', views.log_kill),

    # carrot.js stuff
    url(r'notifications/(?P<app_key>.+)/(?P<user_id>.+)/count$', views.unread_count),
    url(r'notifications/(?P<app_key>.+)/(?P<user_id>.+)/unread$', views.unread_logs),
    url(r'notifications/(?P<app_key>.+)/(?P<user_id>.+)/read$', views.mark_as_read),
    url(r'iframe/notifications/(?P<app_key>.+)/(?P<user_id>.+)/', views.render_iframe),
]
