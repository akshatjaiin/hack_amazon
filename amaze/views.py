# django modules
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.sessions.models import Session
from django.shortcuts import  render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse  

# import
import os
import json
from datetime import date
from dotenv import load_dotenv
from datetime import date
 
def get_date():
    # return current date
    return date.today() 

load_dotenv() # load env
api_key=os.getenv('CHATGPT_API') # cofiguring model api 

def index(request):
    return render(request, "amaze/index.html")