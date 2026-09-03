from django.db import migrations


LODGITECH = {
    'slug': 'lodgitech',
    'title': 'LodgiTech',
    'project_type': 'Responsive UI · Hotel learning project',
    'summary': (
        'A Flutter hotel management interface built to explore how one product '
        'can adapt cleanly across desktop, tablet, and mobile layouts.'
    ),
    'features': [
        'Flexible and Expanded distribute available space without fixed dimensions',
        'LayoutBuilder and MediaQuery switch layouts at practical breakpoints',
        'Responsive font sizing preserves hierarchy and readability on every screen',
    ],
    'tech_stack': 'Flutter, Dart, Responsive UI, Adaptive layouts',
    'source_url': 'https://github.com/AfraimElkesEleia/LodgiTech',
    'image_path': 'images/lodgitech-project-banner.png',
    'image_alt': (
        'LodgiTech hotel interface shown across desktop, tablet, and mobile layouts'
    ),
    'featured': True,
    'display_order': 3,
}


def add_lodgitech(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    slug = LODGITECH['slug']
    defaults = {key: value for key, value in LODGITECH.items() if key != 'slug'}
    Project.objects.update_or_create(slug=slug, defaults=defaults)


def remove_lodgitech(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    Project.objects.filter(slug=LODGITECH['slug']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0002_expand_project_content'),
    ]

    operations = [
        migrations.RunPython(add_lodgitech, remove_lodgitech),
    ]
