from django.shortcuts import render
from django.utils import timezone

from .models import Project


def home(request):
    projects = Project.objects.filter(featured=True)
    return render(
        request,
        'portfolio/home.html',
        {'projects': projects, 'current_year': timezone.now().year},
    )
