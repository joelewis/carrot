from django.http import HttpResponse
from django.shortcuts import render

def user_login(request):
    with open('login.html','r') as file: data=file.readlines()
    return HttpResponse(''.join(data))
