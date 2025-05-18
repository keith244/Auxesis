from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . forms import SquadReportForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from user.models import User
from . models import Squad,SquadReport,SquadReportPhoto
# Create your views here.
User = get_user_model()

def index(request):
    # squad_meeting = get_object_or_404(SquadReportForm,SquadReportPhoto, user)
    squad_meeting = SquadReport.objects.all().order_by('-date')#[:3]
    squad_photo = SquadReportPhoto.objects.all().order_by('-uploaded_at')
    return render(request, 'squad/index.html',{'squad_meeting':squad_meeting})

@login_required(login_url='login')
def squad_report(request):
    if request.method == 'POST':
        form = SquadReportForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                report = form.save(commit=False)
                # report.user = request.user
                report.squad = Squad.objects.get(shepherd = request.user)
                report.save()
                files = request.FILES.getlist('photos')
                for f in files:
                    SquadReportPhoto.objects.create(report=report, images=f)
                messages.success(request,'Report sent successfully!')
                return redirect('squad-report')
            else:
                messages.error(request,'Form validation failed. Please check the erros below!')
        except Exception as e:
            messages.error(request,f'Error! You must be part of a squad to send a report!')
            print(f'Fail: {e}')
            
    else:
        form = SquadReportForm()
    return render(request, 'squad/squad_meeting.html', {'form':form})