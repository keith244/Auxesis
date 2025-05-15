from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
# Create your models here.
class Nation(models.Model):
    name = models.CharField(max_length=100)
    community_shepherd = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Squad(models.Model):
    name = models.CharField(max_length=100)
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    shepherd = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class SquadMeeting(models.Model):
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE)
    date = models.DateField()
    attendees = models.TextField(help_text="List of attendees")
    newcomers = models.TextField(blank=True)
    highlights = models.TextField()
    testimonies = models.TextField(blank=True)
    photo = models.ImageField(upload_to='squad_photos/', blank=True, null=True)
    total_attendees = models.IntegerField()

    class Meta:
        ordering = ['-date']