from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt 

# Create your views here.

def index (request):
    return render (request, 'index.html')

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'wall_messages': Wall_Message.objects.all()
    }
    return render(request, 'success.html', context)


def register(request):
    print(request.POST)
    errors = User.objects.validator(request.POST)
    print(errors)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    #hash the password
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    #new user
    new_user = User.objects.create (first_name=request.POST['first_name'], last_name=request.POST['last_name'], 
    email=request.POST['email'], password=hashed_pw)
    request.session['user'] = new_user.first_name
    request.session['id'] = new_user.id
    return redirect('/success')

def login(request):
    print(request.POST)
    #gets user from database
    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if logged_user.password == request.POST['password']:
            request.session['user'] = logged_user.first_name
            request.session['id'] = logged_user.id
            return redirect('/success')
    return redirect('/')

def logout(request):
    print(request.session)
    request.session.flush()
    print(request.session)
    return redirect('/')


#Left off on editing logic for posting a messsage

def post_mess(request):
    Wall_Message.objects.create(message=request.POST['new_post'], poster=User.objects.get(id=request.session['id']))
    return redirect('/success')
