# Generated by Django 3.1.4 on 2021-02-01 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elearningapp', '0023_auto_20210201_1035'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='solution_text',
            new_name='solution_text_rendered',
        ),
    ]