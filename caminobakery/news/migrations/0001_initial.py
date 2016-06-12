# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 10:21
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(help_text=b'Limited to 250 characters.', max_length=250)),
                ('slug', models.SlugField(help_text=b'Suggested value automatically generated from name. Must be unique for a given pub date.', unique_for_date=b'pub_date')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('body', models.TextField(help_text=b'A brief description of the item. No HTML is allowed; please use Markdown syntax.')),
                ('body_html', models.TextField(blank=True, editable=False)),
                ('excerpt', models.TextField(blank=True, help_text=b'A brief paragraph or so to entice readers to click to the full story. Used on the news indexes. No HTML is allowed.', null=True)),
                ('status', models.IntegerField(choices=[(1, b'Live'), (2, b'Draft')], default=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='categories.Category')),
                ('lead_photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='story_lead_photo', to='media.Photo')),
            ],
            options={
                'ordering': ('-pub_date',),
                'get_latest_by': 'pub_date',
                'verbose_name_plural': 'Stories',
            },
        ),
    ]
