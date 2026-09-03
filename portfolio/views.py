from django.utils import timezone
from django.views.generic import TemplateView

from .selectors import get_featured_projects


class HomeView(TemplateView):
    template_name = 'portfolio/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            projects=get_featured_projects(),
            current_year=timezone.localdate().year,
        )
        return context
