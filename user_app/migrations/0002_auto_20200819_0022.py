# Generated by Django 3.1 on 2020-08-18 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.TextField(blank=True, verbose_name='Имя'),
        ),
    ]