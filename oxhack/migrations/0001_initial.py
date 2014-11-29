# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=1000)),
                ('answer', models.CharField(max_length=200)),
                ('difficulty', models.IntegerField(choices=[(1, b'Easy'), (2, b'Moderate'), (3, b'Hard')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, choices=[(b'MANSFIELD', b'MAN'), (b'IMPERIAL', b'IMP')])),
                ('latitude', models.FloatField(null=True, verbose_name=b'Latitude', blank=True)),
                ('longitude', models.FloatField(null=True, verbose_name=b'Longitude', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('challenges', models.ManyToManyField(to='oxhack.Challenge')),
                ('college', models.ForeignKey(to='oxhack.College')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='challenge',
            name='college',
            field=models.ForeignKey(to='oxhack.College'),
            preserve_default=True,
        ),
    ]
