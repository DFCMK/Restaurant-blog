# Generated by Django 4.2.10 on 2024-04-01 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_comment_options_alter_comment_author_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Vote',
        ),
    ]