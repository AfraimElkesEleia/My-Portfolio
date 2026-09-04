from django.utils import timezone
from django.views.generic import TemplateView

from .models import Project
from .selectors import get_featured_projects


class HomeView(TemplateView):
    template_name = 'portfolio/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured_projects = list(get_featured_projects())
        context.update(
            projects=[p for p in featured_projects if p.section == Project.Section.SELECTED],
            depi_projects=[p for p in featured_projects if p.section == Project.Section.DEPI],
            iti_projects=[p for p in featured_projects if p.section == Project.Section.ITI],
            current_year=timezone.localdate().year,
        )
        return context
