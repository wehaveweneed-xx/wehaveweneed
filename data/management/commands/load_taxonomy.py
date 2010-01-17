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
            if ' -- ' in name:
                parent_name = ' -- '.join(name.split(' -- ')[:-1])
                parent = Category.objects.get_or_create(
                    name=parent_name, slug=slugify(parent_name))[0]
            else:
                parent = None

            Category.objects.get_or_create(name=name, parent=parent,
                                           slug=slugify(name))

