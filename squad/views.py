from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'squad/index.html')

def squad_meeting(request):
    return render(request, 'squad/squad_meeting.html')