# Generated by Django 3.1.4 on 2021-02-01 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearningapp', '0034_activemacroquestion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='macroquestion',
            name='category',
        ),
        migrations.RemoveField(
            model_name='macroquestion',
            name='course',
        ),
        migrations.RemoveField(
            model_name='seenmacroquestion',
            name='macro_question',
        ),
        migrations.RemoveField(
            model_name='seenmacroquestion',
            name='user',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_group',
        ),
        migrations.AlterField(
            model_name='activequestion',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearningapp.question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='solution_text',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='ActiveMacroQuestion',
        ),
        migrations.DeleteModel(
            name='MacroQuestion',
        ),
        migrations.DeleteModel(
            name='SeenMacroQuestion',
        ),
    ]
