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
    return render(request,'user/login.html', {'form':form})


def iregister(request):
    harvest_group = HarvestGroup.objects.filter(shepherd__isnull=True)  # Only show unassigned squads
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Validate shepherd has squad
            if form.cleaned_data['role'] == 'SHEPHERD' and not form.cleaned_data.get('harvest group'):
                messages.error(request, 'Shepherds must be assigned to a harvest group.')
                return render(request, 'user/register.html', {'form': form, 'harvest_group': harvest_group})
            
            user = form.save()

            if form.cleaned_data['role'] == 'SHEPHERD' and form.cleaned_data.get('harvest_group'):
                harvest_group = form.cleaned_data['harvest_group']
                harvest_group.shepherd = user
                harvest_group.save()
                print(f"Assigned {user.username} to squad {harvest_group.name}")  # Debug

            messages.success(request, 'Account created successfully. You can login now.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form, 'harvest_group': harvest_group})

def ilogout(request):
    logout(request)
    return redirect('login')