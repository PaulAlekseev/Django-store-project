# Generated by Django 4.0.5 on 2022-07-17 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='innercategory',
            name='features',
            field=models.JSONField(blank=True, help_text='features used for filter purpose', null=True),
        ),
    ]