# Generated by Django 4.2.17 on 2024-12-19 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='original_name',
            field=models.CharField(default='aa', max_length=255),
            preserve_default=False,
        ),
    ]