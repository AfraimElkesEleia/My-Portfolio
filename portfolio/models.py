from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=120)
    summary = models.TextField()
    tech_stack = models.CharField(
        max_length=250,
        help_text='Comma-separated technologies, for example: Django, PostgreSQL, Docker',
    )
    live_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    featured = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def technologies(self):
        return [item.strip() for item in self.tech_stack.split(',') if item.strip()]
