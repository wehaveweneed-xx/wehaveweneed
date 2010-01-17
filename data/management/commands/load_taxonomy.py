from __future__ import with_statement
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.template.defaultfilters import slugify
from wehaveweneed.web.models import Category
import os


class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, *args, **options):
        dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        with open(os.path.join(dir, 'taxonomy.csv')) as f:
            categories = [line.replace(",", " -- ") for line in f]

        for name in categories:
            built_name = None
            prev = None

            # Not necesarily the most efficient way to do this, but the
            # taxonomy file is rather small and this only has to be
            # run once
            for part in name.split(' -- '):
                if built_name:
                    built_name += ' -- ' + part
                else:
                    built_name = part

                prev, c = Category.objects.get_or_create(
                    name=built_name, slug=slugify(built_name),
                    parent=prev)
