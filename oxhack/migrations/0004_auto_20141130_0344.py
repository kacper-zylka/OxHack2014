# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oxhack', '0003_auto_20141129_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='challengecompletion',
            name='challengeTest',
            field=models.CharField(default='DefaultCollegeTest', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='challengecompletion',
            name='time',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
