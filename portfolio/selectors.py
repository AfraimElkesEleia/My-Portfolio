from __future__ import annotations

from django.db.models import QuerySet

from .models import Project


PROJECT_CARD_FIELDS = (
    'title',
    'slug',
    'project_type',
    'summary',
    'features',
    'tech_stack',
    'live_url',
    'source_url',
    'image_path',
    'image_url',
    'image_alt',
    'display_order',
)


def get_featured_projects() -> QuerySet[Project]:
    """Return only the project data needed by the homepage."""
    return Project.objects.featured().only(*PROJECT_CARD_FIELDS)
