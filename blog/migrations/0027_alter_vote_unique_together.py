# Generated by Django 4.2.10 on 2024-04-26 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_alter_vote_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set(),
        ),
    ]
