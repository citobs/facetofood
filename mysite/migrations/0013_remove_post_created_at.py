# Generated by Django 4.0.8 on 2022-12-28 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0012_alter_resultall_menu_alter_resultall_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='created_at',
        ),
    ]
