from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


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


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create the new user object but don't save it yet
            new_user = user_form.save(commit=False)
            # set the chosen password, for security reasons, instead of 
            # saving the raw password entered by the user, use the set_password() method
            # of the user model that handles hashing
            new_user.set_password(
                user_form.cleaned_data['password']
                )
            # save the user object
            new_user.save()

            # When users register, create an empty profile associated with them
            Profile.objects.create(user=new_user)
            
            args = {'new_user': new_user}
            return render(
                request, 
                'account/register_done.html',
                args
                )
            
    else:
        user_form = UserRegistrationForm()

    args1 = {'user_form': user_form}
    return render(
        request,
        'account/register.html',
        args1)

# view to edit the user profile
# decorator mentioning a login is required before the user can edit the profile details
@login_required         
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
                                instance=request.user,
                                data=request.POST
                                )
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES
                                    )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated sucessfully')
        else:
            messages.error(request, 'Error updating your profile!')
    
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    args = {
        'user_form': user_form,
        'profile_form': profile_form
        }

    return render(request,
                'account/edit.html',
                args)