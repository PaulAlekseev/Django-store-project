# Generated by Django 4.0.5 on 2022-07-29 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_category_image_alter_innercategory_image_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PriceStory',
        ),
    ]