from django.db import models
from tinymce.models import HTMLField
import re
from django.contrib.auth.models import User
# Create your models here.
class Nation(models.Model):
    name = models.CharField(max_length=100)
    community_shepherd = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name.upper()} NATION'
    class Meta:
        verbose_name_plural = 'Nation'

class Squad(models.Model):
    name = models.CharField(max_length=100)
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    shepherd = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name.upper()} -- {self.nation.name}-- {self.shepherd}'
    class Meta:
        verbose_name_plural = 'Squad'

class SquadReport(models.Model):
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE)
    date = models.DateField()
    attendees = models.TextField(help_text="List of attendees")
    visitors = models.TextField(blank=True)
    highlights = models.TextField()
    testimonies = models.TextField(blank=True)
    offering = models.IntegerField()

    def __str__(self):  
        return f'{self.squad.name} Squad report for {self.date}'

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

class SquadReportPhoto(models.Model):
    report = models.ForeignKey(SquadReport, on_delete=models.CASCADE, related_name='photos')
    images = models.ImageField(upload_to='squad_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.images} uploaded {self.report.squad.name.upper()}'