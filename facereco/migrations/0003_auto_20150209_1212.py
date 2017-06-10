# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('facereco', '0002_auto_20150209_0733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='photo',
        ),
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.FileField(default=datetime.datetime(2015, 2, 9, 12, 12, 40, 115936, tzinfo=utc), upload_to=b'tmp/'),
            preserve_default=False,
        ),
    ]
