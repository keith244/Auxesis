from django.shortcuts import render,redirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

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
    return render(request,'user/login.html', {'form':form})


def iregister(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created successfully. You can login now.')
            # return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html',{'form':form})

def ilogout(request):
    logout(request)
    return redirect('login')