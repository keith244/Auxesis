from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import HarvestGroupReportForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import HarvestGroup, HarvestGroupReport, HarvestGroupReportPhoto, Community,MissionalLocation
# Create your views here.
User = get_user_model()


@login_required(login_url='login')
def index(request):
    profile = request.user.profile
    leads_nothing = (
        not HarvestGroup.objects.filter(shepherd=profile).exists()
        and not Community.objects.filter(community_shepherd=profile).exists()
        and not MissionalLocation.objects.filter(leader=profile).exists()
    )
    if leads_nothing:
        messages.error(request,'You dont have a group to lead.')
    else:
        hg = HarvestGroup.objects.filter(shepherd=profile).first()
        cs = Community.objects.filter(community_shepherd=profile).first()
        mls = MissionalLocation.objects.filter(leader=profile).first()

        if mls:
            messages.success(request, f'You lead {mls.name} Missional Location')
        elif cs:
            messages.success(request, f'You lead {cs.name} Community')
        elif hg:
            messages.success(request, f'You lead {hg.name} Harvest Group')



    harvest_group_meeting = HarvestGroupReport.objects.all().order_by('-date')
    harvest_group_photo = HarvestGroupReportPhoto.objects.all().order_by('-uploaded_at')
    return render(request, 'squad/index.html', {'harvest_group_meeting': harvest_group_meeting})


@login_required(login_url='login')
def harvest_group_report(request):
    # Check if user has an assigned harvest group
    try:
        user_harvest_group = HarvestGroup.objects.get(shepherd=request.user.profile)
    except HarvestGroup.DoesNotExist:
        messages.error(request, 'You must be assigned to a harvest group to submit reports.')  
        return redirect('index')
    
    if request.method == 'POST':
        form = HarvestGroupReportForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            # Try to get or create the report
            report, created = HarvestGroupReport.objects.get_or_create(
                harvestgroup=user_harvest_group,
                date=data['date'],
                defaults={
                    'attendees': data['attendees'], 
                    'visitors': data['visitors'], 
                    'highlights': data['highlights'], 
                    'testimonies': data['testimonies'], 
                    'offering': data['offering']
                }
            )
            if not created:
                messages.error(request, 'A report for this date already exists.')  
                return redirect('harvest-group-report')
            
            # Save photos if created
            files = request.FILES.getlist('photos')
            for f in files:
                HarvestGroupReportPhoto.objects.create(report=report, images=f)

            messages.success(request, 'Report sent successfully!')  
            return redirect('harvest-group-report')
        else:
            messages.error(request, 'Form validation failed. Please check the errors below.')  
    else:
        form = HarvestGroupReportForm()
    
    return render(request, 'squad/harvest_group_meeting.html', {'form': form})


@login_required
def manage_harvest_groups(request):
    if request.user.profile.role != 'CS':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        community_id = request.POST.get('community')
        
        if name and community_id:
            HarvestGroup.objects.create(name=name, community_id=community_id)
            messages.success(request, 'Harvest Group created successfully.')
    
    communities = Community.objects.filter(community_shepherd=request.user.profile)
    unassigned_harvest_groups = HarvestGroup.objects.filter(
        shepherd__isnull=True, 
        community__in=communities
    )

    return render(request, 'squads/manage_harvest_groups.html', {
        'communities': communities,
        'unassigned_harvest_groups': unassigned_harvest_groups,
    })


def view_all_meetings(request):
    reports = HarvestGroupReport.objects.all().order_by('-date')
    return render(request,'squad/view_all_reports.html',{'reports':reports})

def leadership_application(request):
    return render (request, 'squad/leadership_application.html')