from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import myTodoForm
from .models import myTodo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'mytodo/home.html')
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'mytodo/signupuser.html', {'form':UserCreationForm()})
    else:
#Create a new User
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'mytodo/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'mytodo/signupuser.html', {'form': UserCreationForm(), 'error':'Passwords did not match'})
    #Tell the user the password

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'mytodo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'mytodo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'mytodo/createtodo.html', {'form': myTodoForm()})
    else:
        try:
            form = myTodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'mytodo/createtodo.html', {'form':myTodoForm(), 'error':'Bad data passed in. Try again'})

@login_required
def currenttodos(request):
    todos = myTodo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'mytodo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = myTodo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'mytodo/completedtodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(myTodo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = myTodoForm(instance=todo)
        return render(request, 'mytodo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = myTodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'mytodo/viewtodo.html', {'todo':todo, 'form':form, 'error': 'Bad info'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(myTodo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(myTodo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')