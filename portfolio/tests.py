from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Project


class ProjectModelTests(TestCase):
    def test_technologies_are_normalized(self):
        project = Project(tech_stack='Flutter,  Supabase, , Cubit ')

        self.assertEqual(project.technologies, ['Flutter', 'Supabase', 'Cubit'])

    def test_features_require_non_empty_strings(self):
        project = Project(
            title='Invalid project',
            slug='invalid-project',
            summary='Summary',
            features=['Valid feature', ''],
            tech_stack='Flutter',
        )

        with self.assertRaises(ValidationError):
            project.full_clean()


class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.all().delete()
        cls.first = Project.objects.create(
            title='First project',
            slug='first-project',
            project_type='Mobile application',
            summary='A focused first project.',
            features=['Feature one', 'Feature two'],
            tech_stack='Flutter, Supabase',
            source_url='https://github.com/example/first-project',
            image_path='images/first-project.png',
            image_alt='First project preview',
            featured=True,
            display_order=1,
        )
        Project.objects.create(
            title='Hidden project',
            slug='hidden-project',
            project_type='Experiment',
            summary='This should not be rendered.',
            features=['Hidden feature'],
            tech_stack='Django',
            featured=False,
            display_order=0,
        )

    def test_homepage_renders_featured_projects_from_the_database(self):
        with self.assertNumQueries(1):
            response = self.client.get(reverse('portfolio:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.first.title)
        self.assertContains(response, 'Feature two')
        self.assertContains(response, 'Supabase')
        self.assertContains(response, self.first.source_url)
        self.assertNotContains(response, 'Hidden project')
        self.assertEqual(response.context['current_year'], timezone.localdate().year)

    def test_featured_projects_use_display_order(self):
        second = Project.objects.create(
            title='Second project',
            slug='second-project',
            project_type='Mobile application',
            summary='A second project.',
            features=['Feature'],
            tech_stack='Kotlin',
            featured=True,
            display_order=0,
        )

        response = self.client.get(reverse('portfolio:home'))

        self.assertEqual(list(response.context['projects']), [second, self.first])
