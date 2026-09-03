from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'featured', 'display_order', 'created_at')
    list_editable = ('featured', 'display_order')
    list_filter = ('featured', 'project_type')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'tech_stack')
    list_per_page = 25
