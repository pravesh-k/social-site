from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


# view for basic user login
def user_login(request):
    if request.method == 'POST':        # if request is POST, pass the form data to form,
        form = LoginForm(request.POST)  
        if form.is_valid():             # check for form validity, and then create user object of authenticate
            cd = form.cleaned_data  
            user = authenticate(        # pass the collected username and password from the form to the authenticate method
                                request,
                                username=cd['username'],
                                password=cd['password']
                                )
            if user:                    # if user object is not null, and is active user
                if user.is_active:      
                    login(request, user)    #pass the user object to login method
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')     # ! Currently this case is not working
            else:
                return HttpResponse('Invalid credentials')      # if user is null, return invalid creds
        
    else:                               # id request method is GET, render an empty LoginForm
        form = LoginForm()

    args = {'form': form}               # create a dictionary and store the form object
    return render(request, 'account/login.html', args)

# view to display after a successful user login
@login_required     #this decorator checks whether the current user is authenticated
def dashboard(request):

    args = {
        'section': 'dashboard'          # section/menu to display the welcome data
        }
    return render(
        request, 
        'account/dashboard.html',       # render the data to the dashboard
        args
        )