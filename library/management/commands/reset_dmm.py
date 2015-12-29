from django.core.management.base import BaseCommand, CommandError
from library.models import *

import sys
sys.path.insert(0, '/home/ec2-user/JAV-scraper')

from DMM import DMM

class Command(BaseCommand):
    help = 'Clears the DMM website'

    def add_arguments(self, parser):
        parser.add_argument('article', type=str)
        parser.add_argument('id', nargs='+', type=int)

    def handle(self, *args, **options):

        article = options['article']

        if article != 'maker':
            self.stdout.write("Error: %s Only maker is supported now" % (article,))
            return

        for a_id in options['id']:
            self.stdout.write("Deleting works from %s %s ..."  % (article,a_id))
            Video.objects.filter(**{ "%s__pk" % article : a_id }).delete()
        
        self.stdout.write("Done")

        return
