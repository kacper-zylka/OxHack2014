# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oxhack', '0006_remove_userprofile_collegetext'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challengecompletion',
            name='user',
        ),
        migrations.AddField(
            model_name='challengecompletion',
            name='userProfile',
            field=models.ForeignKey(default='', to='oxhack.UserProfile'),
            preserve_default=False,
        ),
    ]
