# Generated by Django 4.2.10 on 2024-05-01 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_post_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='approved',
        ),
    ]