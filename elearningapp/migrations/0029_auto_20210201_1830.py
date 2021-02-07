# Generated by Django 3.1.4 on 2021-02-01 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearningapp', '0028_auto_20210201_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='activequestion',
            name='macro_question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearningapp.macroquestion'),
        ),
        migrations.AlterField(
            model_name='activequestion',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearningapp.question'),
        ),
    ]