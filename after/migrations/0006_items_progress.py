# Generated by Django 5.1.7 on 2025-04-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('after', '0005_alter_items_pin_alter_items_user_alter_items_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='progress',
            field=models.IntegerField(blank=True, null=True, verbose_name='progress(%)'),
        ),
    ]
