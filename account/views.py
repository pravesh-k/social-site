from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm


# view for basic user login
def user_login(request):
    if request.mwthod == 'POST':
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
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        
    else:
        form = LoginForm()

    args = {'form': form}
    return render(request, 'account/login.html', args)