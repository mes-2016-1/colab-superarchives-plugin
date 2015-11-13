#!/usr/bin/env python

from django.core.management.base import BaseCommand
from colab_superarchives.models import Thread


class Command(BaseCommand):
    help = "Update keywords used in tag cloud and related thread"

    def handle(self, *args, **kwargs):
        for thread in Thread.objects.iterator():
            thread.update_keywords()
