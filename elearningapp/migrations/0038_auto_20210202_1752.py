# Generated by Django 3.1.4 on 2021-02-02 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearningapp', '0037_auto_20210202_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='answers_per_question',
        ),
        migrations.RemoveField(
            model_name='course',
            name='language',
        ),
        migrations.RemoveField(
            model_name='course',
            name='setup_completed',
        ),
        migrations.AlterField(
            model_name='category',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='elearningapp.course'),
        ),
    ]
