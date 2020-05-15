# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm

from app.firebase_helper import firebase

auth = firebase.auth()

db = firebase.database()

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            print("Email is "+email)
            print("Password is "+password)

            try:
                user = auth.sign_in_with_email_and_password(email, password)
                session_id = user['idToken']
                print(session_id)
                request.session['uid'] = str(session_id)
                return render(request, "index.html", {} )
            except:
                msg = "Email or password might be incorrect"
                return render(request, "accounts/login.html", {"form": form, "msg" : msg})
        
        else:
            msg = 'Error validating the form' 
            return render(request, "accounts/login.html", {"form": form, "msg" : msg})

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })
