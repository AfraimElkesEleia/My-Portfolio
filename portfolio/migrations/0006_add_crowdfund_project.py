from django.db import migrations


def add_crowdfund_project(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    Project.objects.using(schema_editor.connection.alias).update_or_create(
        slug='iti-web-development-project',
        defaults={
            'title': 'CrowdFund',
            'project_type': 'Full-stack web application · ITI final project',
            'summary': (
                'A crowdfunding platform built during ITI Summer Training, '
                'where users can launch campaigns, support projects, and follow funding progress.'
            ),
            'features': [
                'Account registration with email activation and personal profiles',
                'Campaign creation, donations, and funding progress tracking',
                'Project ratings, comments, and reports for community feedback',
            ],
            'tech_stack': 'Python, Django, PostgreSQL, Bootstrap, JavaScript',
            'source_url': 'https://github.com/AfraimElkesEleia/ITI-SummerTraining-FullStack-Crowdfunding',
            'live_url': '',
            'image_path': 'images/iti-crowdfund-project-banner.png',
            'image_url': '',
            'image_alt': (
                'CrowdFund ITI Summer Training banner showing fundraising campaigns, '
                'a donation form, and a project funding dashboard'
            ),
            'section': 'iti',
            'is_mock': False,
            'featured': True,
            'display_order': 1,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0005_add_iti_training_project'),
    ]

    operations = [
        migrations.RunPython(add_crowdfund_project, migrations.RunPython.noop),
    ]
