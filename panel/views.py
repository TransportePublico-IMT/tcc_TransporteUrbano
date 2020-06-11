import json
import urllib

import requests
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from . import plots

@login_required
def home(request):
    return render(request, "panel/home.html",{"page_title": "Dashboard"})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"