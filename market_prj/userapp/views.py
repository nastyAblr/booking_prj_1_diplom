from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from userapp.forms import (CustomUserRegisterForm,
                           CustomUserLoginForm,
                           CustomUserUpdateForm,
                           CustomUserProfileUpdateForm)
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from userapp.forms import CustomUserUpdateForm, CustomUserProfileUpdateForm
from userapp.models import CustomUserProfile
from django.conf import settings


def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('userapp:login')
    else:
        form = CustomUserRegisterForm()
    return render(request, 'userapp/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'userapp/profile.html')


def login(request):
    title = 'вход'

    login_form = CustomUserLoginForm(data=request.POST or None)

    next_page = request.GET.get('next', '')

    if request.method == 'POST' and login_form.is_valid():

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            auth_login(request, user)

            if request.POST.get('next'):
                return redirect(request.POST.get('next'))

            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'userapp/login.html', {
        'title': title,
        'login_form': login_form,
        'next': next_page,
    })


def logout(request):
    auth_logout(request)
    return redirect('userapp:login')


@login_required
def profile_edit(request):
    user = request.user

    profile, created = CustomUserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(
            request.POST,
            request.FILES,
            instance=user
        )
        profile_form = CustomUserProfileUpdateForm(
            request.POST,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('userapp:profile')

    else:
        user_form = CustomUserUpdateForm(instance=user)
        profile_form = CustomUserProfileUpdateForm(instance=profile)

    return render(request, 'userapp/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
