# -*- coding: utf-8 -*-

#Django imports
from django.core.management.base import BaseCommand, CommandError

#Python imports


#Project import
from callcenter.models import PrecomputeData

class Command(BaseCommand):
    def handle(self, *args, **options):
        PrecomputeData.objects.filter(code="dcalls").update(integer_value=0)
