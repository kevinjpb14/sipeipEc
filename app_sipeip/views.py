from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def hello(request):
    return HttpResponse("Hola Mundo")


def login_view(request):
    return render(request, 'app_sipeip/login.html')