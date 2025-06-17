from django.contrib import admin
from . models import Community, HarvestGroup, HarvestGroupReport, HarvestGroupReportPhoto, MissionalLocation
import csv
from django.utils.html import format_html

@admin.register(MissionalLocation)
class MissionalLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'community_count')
    list_filter = ('leader',)
    search_fields = ('name',)
    
    def community_count(self, obj):
        return obj.community_set.count()
    community_count.short_description = 'Communities'

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'missional_location', 'community_shepherd', 'harvestgroup_count')
    list_filter = ('missional_location', 'community_shepherd',)
    search_fields = ('name',)
    
    def harvestgroup_count(self, obj):
        return obj.harvestgroup_set.count()  # Fixed: harvestgroup_set instead of squad_set
    harvestgroup_count.short_description = 'Harvest Groups'

@admin.register(HarvestGroup)
class HarvestGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'community', 'shepherd', 'has_shepherd', 'report_count')
    list_filter = ('community', 'shepherd')
    search_fields = ('name', 'community__name')  # Fixed: community__name instead of nation__name
    actions = ['clear_shepherd']
    
    def has_shepherd(self, obj):
        return obj.shepherd is not None
    has_shepherd.boolean = True
    has_shepherd.short_description = 'Assigned'
    
    def report_count(self, obj):
        return obj.harvestgroupreport_set.count()
    report_count.short_description = 'Reports'
    
    def clear_shepherd(self, request, queryset):
        queryset.update(shepherd=None)
        self.message_user(request, f'{queryset.count()} Harvest Groups cleared of shepherds.')
    clear_shepherd.short_description = 'Clear shepherd assignment'

class HarvestGroupReportPhotoInline(admin.TabularInline):
    model = HarvestGroupReportPhoto
    readonly_fields = ['display_image']
    fields = ['images', 'display_image']
    extra = 1

    def display_image(self, obj):
        if obj.images:
            return format_html(
                '<img src="{}" width="100" height="auto" />',obj.images.url
            )
        return "No image"
    display_image.short_description = 'Image Preview'

@admin.register(HarvestGroupReport)  # Fixed: HarvestGroupReport instead of SquadReport
class HarvestGroupReportAdmin(admin.ModelAdmin):
    inlines = [HarvestGroupReportPhotoInline]  # Fixed: removed duplicate "PhotoInline"
    list_display = ('harvestgroup','date','get_attendee_count','get_visitor_count','offering','display_photos')  # Fixed: harvestgroup instead of squad
    list_filter = ('date', 'harvestgroup__community', 'harvestgroup')  # Fixed: harvestgroup__community instead of squad__nation
    search_fields = ('harvestgroup__name',)  # Fixed: harvestgroup__name instead of squad__name
    date_hierarchy = 'date'

    def display_photos(self,obj):
        photos = obj.photos.all()
        if photos:
            html = '<div style="display: flex; gap: 5px">'
            for photo in photos:
                html += format_html(
                    '<img src="{}" width="50" height="auto" />',photo.images.url
                )
            html += '</div>'
            return format_html(html)
        return "No photos"
    
    display_photos.short_description = "Photos"