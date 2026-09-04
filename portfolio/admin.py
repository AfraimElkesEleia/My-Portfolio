from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'project_type', 'is_mock', 'featured', 'display_order', 'created_at')
    list_editable = ('section', 'is_mock', 'featured', 'display_order')
    list_filter = ('section', 'is_mock', 'featured', 'project_type')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'tech_stack')
    list_per_page = 25
