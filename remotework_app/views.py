import os
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from.forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login 
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from .utils import generate_employee_id
from .models import Task
from django.contrib.auth.decorators import login_required





def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print (form)

        if form.is_valid():
            # Hash the password before saving
            user = form.save(commit=False)
            user.empid = generate_employee_id()
            user.save()
            messages.success(request, 'You have successfully registered! Please log in to continue.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def Login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email= form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # redirect to dashboard page
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database. See below for a real example I wrote for Photon Designer.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data

    return redirect('login')


def sign_out(request):
    del request.session['user_data']
    return redirect('login')



@login_required
def filter_tasks(request):
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    search_query = request.GET.get('search')
    tasks = Task.objects.filter(assigned_to=request.user)
    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)
    if search_query:
        tasks = tasks.filter(title__icontains=search_query) | tasks.filter(description__icontains=search_query)
    return render(request, 'dashboard.html', {'tasks': tasks})


@login_required
def Index(request):
    tasks = Task.objects.all()
    for task in tasks:
        print(task.title)
    return render(request, 'index.html', {'tasks': tasks})