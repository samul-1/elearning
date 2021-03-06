# Generated by Django 3.1.7 on 2021-03-05 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearningapp', '0002_coursepermission_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AddConstraint(
            model_name='answer',
            constraint=models.UniqueConstraint(fields=('question', 'answer_index'), name='unique_answer_index_question'),
        ),
        migrations.AddConstraint(
            model_name='answer',
            constraint=models.UniqueConstraint(fields=('question', 'text'), name='unique_answer_text'),
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('course', 'name'), name='unique_category_course'),
        ),
        migrations.AddConstraint(
            model_name='coursepermission',
            constraint=models.UniqueConstraint(fields=('user',), name='unique_user_course_permission'),
        ),
    ]
