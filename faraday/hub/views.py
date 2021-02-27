from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.
@login_required(login_url='login')
def hub(request):
    context = {}
    return render(request, 'hub/hub.html', context)

def registerUserPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Scientist.objects.create(user=user)
            return redirect('login')
    context = {'form':form, 'type':'fellow scientist'}

    return render(request, 'hub/register.html', context)

def registerEmployerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Employer.objects.create(user=user)
            return redirect('login')
    context = {'form':form, 'type':'enterprise'}

    return render(request, 'hub/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('hub')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('hub')
			
		context = {}
		return render(request, 'hub/login.html', context)

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('hub')

@login_required(login_url='login')
def account(request):
    context = {}
    return render(request, 'hub/account.html', context)

@login_required(login_url='login')
def datapool(request):
    context = {}
    return render(request, 'hub/datapool.html', context)

@login_required(login_url='login')
def dashboard(request):
    context = {}
    return render(request, 'hub/dashboard.html', context)

@login_required(login_url='login')
def references(request):
    context = {}
    return render(request, 'hub/references.html', context)