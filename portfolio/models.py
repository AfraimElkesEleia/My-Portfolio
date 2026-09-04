from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property


def validate_string_list(value):
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ValidationError('Enter a list containing non-empty text values.')


class ProjectQuerySet(models.QuerySet):
    def featured(self):
        return self.filter(featured=True)


class Project(models.Model):
    class Section(models.TextChoices):
        SELECTED = 'selected', 'Selected work'
        DEPI = 'depi', 'DEPI projects'
        ITI = 'iti', 'ITI Summer Training'

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    project_type = models.CharField(max_length=120, default='Mobile application')
    summary = models.TextField()
    features = models.JSONField(default=list, validators=[validate_string_list])
    tech_stack = models.CharField(
        max_length=250,
        help_text='Comma-separated technologies, for example: Django, PostgreSQL, Docker',
    )
    live_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    image_path = models.CharField(
        max_length=255,
        blank=True,
        help_text='Path inside static files, for example: images/project-banner.png',
    )
    image_url = models.URLField(blank=True)
    image_alt = models.CharField(max_length=255, blank=True)
    section = models.CharField(
        max_length=20, choices=Section.choices, default=Section.SELECTED,
    )
    is_mock = models.BooleanField(
        default=False,
        help_text='Label sample content as a mock project until real project details are added.',
    )
    featured = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProjectQuerySet.as_manager()

    class Meta:
        ordering = ['display_order', 'title']
        indexes = [
            models.Index(
                fields=['featured', 'display_order'],
                name='portfolio_featured_order_idx',
            ),
        ]

    def __str__(self):
        return self.title

    @cached_property
    def technologies(self):
        return [item.strip() for item in self.tech_stack.split(',') if item.strip()]

    @property
    def primary_url(self):
        return self.live_url or self.source_url

    @property
    def primary_link_label(self):
        return 'View live project' if self.live_url else 'View repository'
