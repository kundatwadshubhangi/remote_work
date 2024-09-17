import os
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from.forms import RegistrationForm, TaskForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import Task, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods





def generate_employee_id():
    # Implement your logic to generate a unique employee ID here
    import random
    return str(random.randint(10000000, 99999999))


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(request.POST)  # Add this to debug
        if form.is_valid():
            print("valid")
            user = form.save(commit=False)
            user.empid = generate_employee_id()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'You have successfully registered! Please log in to continue.')
            return redirect('login')
        else:
            print("Errors in username:", form.errors.get('username'))
            print("Errors in email:", form.errors.get('email'))
            print("Errors in first_name:", form.errors.get('first_name'))
            print("Errors in last_name:", form.errors.get('last_name'))
            print("Errors in role:", form.errors.get('role'))
            print("Errors in date_joined:", form.errors.get('date_joined'))
            print("Errors in last_login:", form.errors.get('last_login'))
            print("Errors in is_staff:", form.errors.get('is_staff'))
            print("Errors in is_active:", form.errors.get('is_active'))
            print("Errors in is_superuser:", form.errors.get('is_superuser'))
            print("Errors in password1:", form.errors.get('password1'))
            print("Errors in confirm_password:", form.errors.get('password2'))
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def Login_view(request):
    if request.method == 'POST':
        print("Post method")
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            return redirect('index')  # redirect to index page
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


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


# logout page
def user_logout(request):
    logout(request)
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
    tasks = Task.objects.filter(assigned_to=request.user)
    for task in tasks:
        print(task.title)
        task.task_id = task.id
    return render(request, 'index.html', {'tasks': tasks})


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # redirect to task list page
    else:
        form = TaskForm()
        users = User.objects.all()  # Get all users
    return render(request, 'new_task.html', {'form': form, 'users': users})


def get_task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    data = {
        'title': task.title,
        'description': task.description,
        'assigned_to': {'id': task.assigned_to.id, 'username': task.assigned_to.username},
        'status': task.status,
        'priority': task.priority,
        'due_date': task.due_date,
    }
    return JsonResponse(data)

def update_task_details(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.assigned_to = User.objects.get(id=request.POST.get('assigned_to'))  # Assuming assigned_to is a User object
        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        task.due_date = request.POST.get('due_date')
        task.save()
        return JsonResponse({'message': 'Task updated successfully'})
    return JsonResponse({'message': 'Error updating task'})
        
@require_http_methods(['POST'])
def delete_task(request):
    task_id = request.POST.get('task_id')
    # Delete the task with the given task_id
    return JsonResponse({'message': 'Task deleted successfully!'})