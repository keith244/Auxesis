from django.contrib import admin
from . models import Nation, Squad, SquadReport, SquadReportPhoto
import csv
from django.utils.html import format_html
# Register your models here.

admin.site.register(Nation)
admin.site.register(Squad)
# admin.site.register(SquadReport)
# admin.site.register(SquadReportPhoto)

class SquadReportPhotoInline(admin.TabularInline):
    model = SquadReportPhoto
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
class SquadReportAdmin(admin.ModelAdmin):
    inlines = [
        SquadReportPhotoInline,
    ]
    list_display = ('squad','date','offering','display_photos')

    def display_photos (self,obj):
        photos = obj.photos.all()
        if photos:
            html = '<div style = "display: flex; gap: 5px">'
            for photo in photos:
                html += format_html (
                    '<img src="{}" width="150" height="auto" />',photo.images.url
                )
            html += '</div>'
        return "No photos"
    
    display_photos.short_description="Photos"

admin.site.register(SquadReport, SquadReportAdmin)

# class SquadReportPhotoAdmin(admin.ModelAdmin):
#     list_display = ('report','display_image', 'uploaded_at')

#     def display_image(self,obj):
#         if obj.images:
#             return format_html('<img src="{}" width="100" height="auto" />', obj.images.url)
#         return "No image"
#     display_image.short_description = 'Image'
# admin.site.register(SquadReportPhoto, SquadReportPhotoAdmin)
