# Generated by Django 3.1.7 on 2021-03-05 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearningapp', '0003_auto_20210305_0934'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='coursepermission',
            name='unique_user_course_permission',
        ),
        migrations.AddField(
            model_name='coursepermission',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='elearningapp.course'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='coursepermission',
            constraint=models.UniqueConstraint(fields=('user', 'course'), name='unique_user_course_permission'),
        ),
    ]
