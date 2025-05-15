from django.contrib import admin
from . models import Nation, Squad, SquadMeeting

# Register your models here.

admin.site.register(Nation)
admin.site.register(Squad)
admin.site.register(SquadMeeting)