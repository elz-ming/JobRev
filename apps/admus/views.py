# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
# ========== IMPORT-ANTS ========== #

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django import template
from django.template import loader

from django.contrib.auth.models import User
from apps.admus.forms import LoginForm, SignUpForm

# ========== VIEWS ========== #

@login_required(login_url="/login/")
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def login_user(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    msg = 'Your account was inactive'
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "admus/login.html", {"form": form, "msg": msg})

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True
        else:
            msg = 'Invalid form'

        # return redirect("/login/")
    else:
        form = SignUpForm()

    return render(request, "admus/register.html", {"form": form, "msg": msg, "success": success})


