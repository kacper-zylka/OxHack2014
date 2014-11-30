# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('oxhack', '0002_auto_20141129_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengecompletion',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='college',
            name='name',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
