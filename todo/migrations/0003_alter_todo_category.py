# Generated by Django 4.1.4 on 2023-04-14 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
