from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import FileResponse

import csv
from django.contrib.staticfiles.storage import staticfiles_storage

from .models import *
from .forms import *

import os
from django.conf import settings
from django.http import HttpResponse, Http404

from django.templatetags.static import static
# VIEWS
@login_required(login_url='login')
def hub(request):
    json_serializer = serializers.get_serializer("json")()
    dp = json_serializer.serialize(DataPool.objects.all(), ensure_ascii=False)

    numDP = len(DataPool.objects.all())
    numDE = len(DataEntry.objects.all())
    numSC = len(Scientist.objects.all())
    numEM = len(Employer.objects.all())

    ecology = json_serializer.serialize(DataPool.objects.filter(category="Ecology"), ensure_ascii=False)
    sociology = json_serializer.serialize(DataPool.objects.filter(category="Sociology"), ensure_ascii=False)
    astronomy = json_serializer.serialize(DataPool.objects.filter(category="Astronomy"), ensure_ascii=False)
    geology = json_serializer.serialize(DataPool.objects.filter(category="Geology"), ensure_ascii=False)

    context = {"eco":ecology, "soc":sociology, "ast": astronomy, "geo":geology, "DP":numDP, "DE":numDE, "SC":numSC, "EM":numEM}
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

    scientists = Scientist.objects.filter(user=request.user)
    if len(scientists) == 0:
        return redirect('hub')
    scientist = scientists[0]

    entries = DataEntry.objects.filter(scientist__user=request.user)

    status = "Inactive"
    if len(entries)>0:
        status = "Active contributor"

    balance = 0
    all_months = []

    for entry in entries:
        balance+=entry.datapool.prize
        date = str(entry.date_created.month)
        all_months.append(date)

    jan = 0
    feb = 0
    mar = 0
    apr = 0

    for month in all_months:
        if month == '1':
            jan+=1
        elif month == '2':
            feb+=1
        elif month== '3':
            mar+=1
        else:
            apr+=1

    months = [jan, feb, mar, apr]
    print(all_months)
    # json_serializer = serializers.get_serializer("json")()
    # months = json_serializer.serialize(months, ensure_ascii=False)

    context = {"scientist":scientist, "entries":entries, "num":len(entries), "status":status, "balance":balance, "contribs":months}
    return render(request, 'hub/account.html', context)

@login_required(login_url='login')
def datapool(request, pk):
    pk = pk.replace('_', ' ')
    datapool = DataPool.objects.filter(name=pk)[0]

    if request.method == 'POST':
        answers = request.POST.get('answers')
        scientist = Scientist.objects.filter(user=request.user)

        if len(scientist) == 0:
            return redirect('hub')

        scientist = scientist[0]
        print(scientist)
        datapool = DataPool.objects.filter(name=pk)[0]

        # prize = Datapool.objects.get_or_create(name=pk)
        # account, created = Scientist.objects.get_or_create(user=request.user)
        # account.balance+=1
        # scientist.balance+=1

        new_entry = DataEntry.objects.create(scientist=scientist, datapool=datapool, answers=answers)
        # new_entry.save()
        print(new_entry)
        return redirect('hub')

    context = {"name":pk, "datapool":datapool}
    print(datapool.prize)
    return render(request, 'hub/datapool.html', context)

@login_required(login_url='login')
def dashboard(request):

    employer = Employer.objects.filter(user__username=request.user.username)
    print(employer)

    if len(employer) == 0:
        return redirect('hub')
    else:
        employer = employer[0]
    # at this point, employer is the employer (boom)
    datapool = DataPool.objects.filter(employer__user=employer.user)
    print(datapool)
    if len(datapool) == 0:
        # PROMPT THEM TO CREATE A DATAPOOL
        return redirect('createDataPool')
    else:
        dp = datapool[0]

        # BEGIN FUNKY CSV BUSINESS
        dataentries = DataEntry.objects.filter(datapool=dp)

        new_data = []

        for entry in dataentries:
            print(entry.answers.split(','))
            new_data.append(entry.answers.split(','))

        print(dataentries)

        # for entry in dataentries:
        #     print(entry.docURL)
        #     with open('static/images' + entry.document.url) as csvfile:
        #         content = csv.reader(csvfile, delimiter=' ', quotechar='|')
        #         content = list(content)
        #         data.append(content[1])

        print(new_data)
        print("====================================")
        context = {"data":new_data}
        return render(request, 'hub/dashboard.html', context)


    context = {}
    return render(request, 'hub/dashboard.html', context)

def createDataPool(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        questions = request.POST.get('questions')
        cap = request.POST.get('cap')

        employer = Employer.objects.filter(user=request.user)[0]


        new_dp = DataPool.objects.create(name=name,
                                        employer=employer,
                                        description=description,
                                        category=category,
                                        questions=questions,
                                        entry_cap=cap)
        return redirect('hub')

    context = {}
    return render(request, 'hub/create_datapool.html', context)

@login_required(login_url='login')
def references(request):
    context = {}
    return render(request, 'hub/references.html', context)

@login_required(login_url='login')
def download(request, pk):
    obj = DataPool.objects.get(name=pk)
    filename = 'static/images/references' + obj.docURL
    response = FileResponse(open(filename, 'rb'))
    return response
