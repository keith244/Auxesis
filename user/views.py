from django.shortcuts import render,redirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from squad.models import HarvestGroup
# Create your views here.
def ilogin(request):
    form = LoginForm(request.POST or None) 
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate (request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            messages.error(request,'Invalid credentials!')
        else:
            messages.error(request,'PLease correct the form.')
    return render(request,'user/login.html', {'form':form})


def iregister(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,'Account created successfully. You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'There was an error in your form. Please try again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form,})

def ilogout(request):
    logout(request)
    return redirect('login')