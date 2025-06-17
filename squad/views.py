from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import HarvestGroupReportForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import HarvestGroup, HarvestGroupReport, HarvestGroupReportPhoto, Community
# Create your views here.
User = get_user_model()


@login_required(login_url='login')
def index(request):
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
            report = form.save(commit=False)
            report.harvestgroup = user_harvest_group
            report.save()
            
            files = request.FILES.getlist('photos')
            for f in files:
                HarvestGroupReportPhoto.objects.create(report=report, images=f)
            
            messages.success(request, 'Report sent successfully!')
            return redirect('harvest-group-report')
        else:
            messages.error(request, 'Form validation failed. Please check the errors below!')
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