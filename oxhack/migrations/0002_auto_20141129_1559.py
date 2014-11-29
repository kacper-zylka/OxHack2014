# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oxhack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengeCompletion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateField()),
                ('challenge', models.ForeignKey(to='oxhack.Challenge')),
                ('user', models.ForeignKey(to='oxhack.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='challenges',
        ),
        migrations.AlterField(
            model_name='college',
            name='latitude',
            field=models.FloatField(default=0, verbose_name=b'Latitude'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='college',
            name='longitude',
            field=models.FloatField(default=0, verbose_name=b'Longitude'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='college',
            name='name',
            field=models.CharField(max_length=200, choices=[(b'MAN', b'MANSFIELD'), (b'IMP', b'IMPERIAL')]),
            preserve_default=True,
        ),
    ]
