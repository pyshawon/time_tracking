# Generated by Django 3.2.10 on 2022-01-01 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='dateline',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='dateline',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_datetime',
            field=models.DateTimeField(),
        ),
    ]
