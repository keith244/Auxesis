from django.db import models
from tinymce.models import HTMLField
import re
from django.contrib.auth.models import User
from user.models import Profile
# Create your models here.

class MissionalLocation(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
class Community(models.Model):
    name = models.CharField(max_length=100)
    missional_location = models.ForeignKey(MissionalLocation, on_delete=models.CASCADE)
    community_shepherd = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name} Community'
    class Meta:
        verbose_name_plural = 'Communities'
class HarvestGroup(models.Model):
    name = models.CharField(max_length=100)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)  # Renamed from nation
    shepherd = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name} -- {self.community.name}'
    class Meta:
        verbose_name_plural = 'Harvest Groups'

class HarvestGroupReport(models.Model):
    harvestgroup = models.ForeignKey(HarvestGroup, on_delete=models.CASCADE)
    date = models.DateField()
    attendees = models.TextField(help_text="List of attendees")
    visitors = models.TextField(blank=True)
    highlights = models.TextField()
    testimonies = models.TextField(blank=True)
    offering = models.IntegerField()

    def __str__(self):  
        return f'{self.harvestgroup.name} HG report for {self.date}'

    def get_attendee_count(self):
        attendees_list = [name.strip() for name in re.split(r'[,\n]',self.attendees) if name.strip()]
        return len(attendees_list)
    
    def get_visitor_count (self):
        if not self.visitors:
            return 0
        visitors_list = [name.strip() for name in re.split(r'[,\n]', self.visitors) if name.strip()]
        return len(visitors_list)

    class Meta:
        ordering = ['-date']
        unique_together = ['harvestgroup', 'date']

class HarvestGroupReportPhoto(models.Model):
    report = models.ForeignKey(HarvestGroupReport, on_delete=models.CASCADE, related_name='photos')
    images = models.ImageField(upload_to='harvest_group_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.images} uploaded {self.report.harvestgroup.name.upper()}'