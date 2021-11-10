from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


# view for basic user login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                                request,
                                username=cd['username'],
                                password=cd['password']
                                )
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')     # Currently this case is not working
            else:
                return HttpResponse('Invalid credentials')
        
    else:
        form = LoginForm()

    args = {'form': form}
    return render(request, 'account/login.html', args)

# view to display after a successful user login
@login_required     #this decorator checks whether the current user is authenticated
def dashboard(request):

    args = {
        'section': 'dashboard'
        }
    return render(
        request, 
        'account/dashboard.html',
        args
        )