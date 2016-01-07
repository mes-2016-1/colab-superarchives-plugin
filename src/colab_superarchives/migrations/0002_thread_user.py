# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


def saveThreads(apps, schema_editor):
    Thread = apps.get_model('colab_superarchives', 'Thread')
    for t in Thread.objects.all():
        if t.latest_message and t.latest_message.from_address:
            t.user = t.latest_message.from_address.user
        t.save()
    return

def reverseThreads(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('colab_superarchives', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.RunPython(saveThreads, reverseThreads),
    ]
