from django.db import migrations, models
from django.utils.text import slugify

import portfolio.models


PROJECTS = (
    {
        'slug': 'rihla',
        'title': 'Rihla',
        'project_type': 'Graduation project · Mobile application',
        'summary': (
            'A Flutter transportation platform that brings trip planning, seat '
            'booking, digital tickets, and payments into one connected experience.'
        ),
        'features': [
            'Direct, indirect, round-trip, and multi-destination journey search',
            'Real-time seat maps, wallet checkout, and QR boarding passes',
            'Travel alerts, loyalty rewards, and a ticket resale marketplace',
        ],
        'tech_stack': 'Flutter, Bloc / Cubit, REST API, Graduation project',
        'source_url': 'https://github.com/AfraimElkesEleia/Transportation-App-Graduation-Project',
        'image_path': 'images/rihla-project-banner.png',
        'image_alt': 'Rihla mobile transport application presentation',
        'featured': True,
        'display_order': 1,
    },
    {
        'slug': 'voltmarket',
        'title': 'VoltMarket',
        'project_type': 'E-commerce · Mobile application',
        'summary': (
            'An electronics shopping app built with Flutter, using Supabase for '
            'product data and storage while Cubit keeps the experience responsive.'
        ),
        'features': [
            'Product browsing, category filters, details, and customer reviews',
            'Favorites, shopping cart management, and order creation',
            'Firebase sign-in plus Supabase-backed profiles and image storage',
        ],
        'tech_stack': 'Flutter, Supabase, Firebase Auth, Bloc / Cubit',
        'source_url': 'https://github.com/AfraimElkesEleia/VoltMarket',
        'image_path': 'images/voltmarket-project-banner.png',
        'image_alt': 'VoltMarket electronics e-commerce mobile application presentation',
        'featured': True,
        'display_order': 2,
    },
)


def populate_project_content(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    used_slugs = set()

    for project in Project.objects.order_by('pk'):
        base_slug = slugify(project.title) or f'project-{project.pk}'
        candidate = base_slug
        suffix = 2
        while candidate in used_slugs:
            candidate = f'{base_slug}-{suffix}'
            suffix += 1
        project.slug = candidate
        project.save(update_fields=['slug'])
        used_slugs.add(candidate)

    for project_data in PROJECTS:
        slug = project_data['slug']
        defaults = {key: value for key, value in project_data.items() if key != 'slug'}
        Project.objects.update_or_create(slug=slug, defaults=defaults)


def remove_seeded_projects(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    Project.objects.filter(slug__in=[project['slug'] for project in PROJECTS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='features',
            field=models.JSONField(
                default=list,
                validators=[portfolio.models.validate_string_list],
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='image_alt',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='project',
            name='image_path',
            field=models.CharField(
                blank=True,
                help_text='Path inside static files, for example: images/project-banner.png',
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='project_type',
            field=models.CharField(default='Mobile application', max_length=120),
        ),
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(max_length=140, null=True, unique=True),
        ),
        migrations.RunPython(populate_project_content, remove_seeded_projects),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(max_length=140, unique=True),
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['display_order', 'title']},
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(
                fields=['featured', 'display_order'],
                name='portfolio_featured_order_idx',
            ),
        ),
    ]
