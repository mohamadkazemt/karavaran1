# Generated by Django 5.0.6 on 2024-06-25 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0002_course_situation'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
