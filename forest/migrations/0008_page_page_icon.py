# Generated by Django 3.1.1 on 2020-12-16 21:43

from django.db import migrations
import fontawesome_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forest', '0007_auto_20201216_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='page_icon',
            field=fontawesome_5.fields.IconField(blank=True, max_length=60),
        ),
    ]