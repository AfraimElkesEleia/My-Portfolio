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

    def test_depi_projects_are_separate_ordered_and_respect_visibility(self):
        last = Project.objects.create(
            title='Later DEPI project', slug='later-depi', summary='Later training work.',
            tech_stack='Kotlin', section=Project.Section.DEPI, display_order=2,
        )
        first = Project.objects.create(
            title='First DEPI project', slug='first-depi', summary='First training work.',
            tech_stack='Kotlin', section=Project.Section.DEPI, display_order=1,
        )
        Project.objects.create(
            title='Hidden DEPI project', slug='hidden-depi', summary='Hidden training work.',
            tech_stack='Kotlin', section=Project.Section.DEPI, featured=False,
        )

        with self.assertNumQueries(1):
            response = self.client.get(reverse('portfolio:home'))

        self.assertEqual(response.context['projects'], [self.first])
        self.assertEqual(response.context['depi_projects'], [first, last])
        self.assertContains(response, 'id="depi-projects"')
        self.assertNotContains(response, 'Hidden DEPI project')

    def test_repository_card_handles_mock_and_real_project_without_screenshots(self):
        project = Project.objects.create(
            title='DEPI sample', slug='depi-sample', summary='Sample mobile project.',
            tech_stack='Kotlin, Room', section=Project.Section.DEPI, is_mock=True,
        )

        response = self.client.get(reverse('portfolio:home'))
        card = response.content.decode().split('aria-labelledby="depi-sample-title">')[1].split('</article>')[0]
        self.assertIn('Mock project', card)
        self.assertIn('Repository coming soon', card)
        self.assertNotIn('<a ', card)
        self.assertNotIn('<img', card)

        project.source_url = 'https://github.com/example/depi-sample'
        project.is_mock = False
        project.save()
        response = self.client.get(reverse('portfolio:home'))
        card = response.content.decode().split('aria-labelledby="depi-sample-title">')[1].split('</article>')[0]
        self.assertIn(f'href="{project.source_url}"', card)
        self.assertIn('View repository', card)
        self.assertNotIn('Mock project', card)
        self.assertNotIn('Repository coming soon', card)
        self.assertNotIn('<img', card)

    def test_iti_mock_project_is_separate_from_other_work(self):
        iti = Project.objects.create(
            title='ITI sample', slug='iti-sample', summary='Summer training project.',
            tech_stack='Python, Django, Flask', section=Project.Section.ITI, is_mock=True,
        )
        depi = Project.objects.create(
            title='DEPI sample', slug='depi-sample', summary='Mobile training project.',
            tech_stack='Kotlin', section=Project.Section.DEPI,
        )
        Project.objects.create(
            title='Hidden ITI project', slug='hidden-iti', summary='Not ready yet.',
            tech_stack='Django', section=Project.Section.ITI, featured=False,
        )

        with self.assertNumQueries(1):
            response = self.client.get(reverse('portfolio:home'))

        self.assertEqual(response.context['projects'], [self.first])
        self.assertEqual(response.context['depi_projects'], [depi])
        self.assertEqual(response.context['iti_projects'], [iti])
        self.assertContains(response, 'id="iti-projects"')
        self.assertContains(response, 'aria-labelledby="iti-sample-title"', count=1)
        self.assertContains(response, '01 project</span>')
        self.assertNotContains(response, 'Hidden ITI project')
        card = response.content.decode().split('aria-labelledby="iti-sample-title">')[1].split('</article>')[0]
        self.assertIn('Mock project', card)
        self.assertIn('Repository coming soon', card)
        self.assertIn('Django', card)
        self.assertIn('Flask', card)
        self.assertNotIn('<a ', card)

    def test_no_empty_training_sections_or_broken_journey_link(self):
        response = self.client.get(reverse('portfolio:home'))

        self.assertNotContains(response, 'id="depi-projects"')
        self.assertNotContains(response, 'href="#depi-projects"')
        self.assertNotContains(response, 'id="iti-projects"')

    def test_iti_project_with_banner_uses_featured_layout_and_repository_link(self):
        project = Project.objects.create(
            title='CrowdFund', slug='crowdfund', summary='A fundraising platform.',
            tech_stack='Django, PostgreSQL', section=Project.Section.ITI,
            source_url='https://github.com/example/crowdfund',
            image_path='images/iti-crowdfund-project-banner.png',
            image_alt='CrowdFund campaign and donation screens',
        )

        response = self.client.get(reverse('portfolio:home'))
        section = response.content.decode().split('id="iti-projects"')[1].split('</section>')[0]
        self.assertIn('class="featured-project reveal"', section)
        self.assertIn(f'src="/static/{project.image_path}"', section)
        self.assertIn(f'alt="{project.image_alt}"', section)
        self.assertIn('<h4>CrowdFund</h4>', section)
        self.assertIn(f'href="{project.source_url}"', section)
        self.assertNotIn('Mock project', section)
        self.assertNotIn('Repository coming soon', section)
        self.assertNotIn('View live project', section)
