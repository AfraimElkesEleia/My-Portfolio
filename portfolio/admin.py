from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'display_order', 'created_at')
    list_editable = ('featured', 'display_order')
    list_filter = ('featured',)
    search_fields = ('title', 'summary', 'tech_stack')
