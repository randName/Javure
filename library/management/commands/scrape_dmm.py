from django.core.management.base import BaseCommand, CommandError
from library.models import *

import sys
sys.path.insert(0, '/home/ec2-user/JAV-scraper')

from DMM import DMM

class Command(BaseCommand):
    help = 'Scrapes the DMM website'

    def add_arguments(self, parser):
        parser.add_argument('scrape_targets', nargs='+', type=str)

    def handle(self, *args, **options):

        dmm = DMM()

        for target in options['scrape_targets']:
            if target == 'keywords':
                self.stdout.write("Scraping keywords from DMM...")

                for k in dmm.get_keywords(): Keyword.objects.get_or_create(**k)

            elif target == 'makers':
                self.stdout.write("Scraping makers from DMM...")

                for mora in dmm.MORAS:
                    self.stdout.write( mora, ending="\r" )
                    dmm.get_makers(mora, callback=lambda x: Maker.objects.get_or_create(**x) )

            elif target == 'actresses':
                self.stdout.write("Scraping actresses from DMM...")

                for mora in dmm.MORAS:
                    self.stdout.write( mora, ending="\r" )
                    dmm.get_actresses(mora, callback=lambda x: Actress.objects.get_or_create(**x) )

            else:
                self.stdout.write("Error: Scrape target '%s' not recognised" % target)

        self.stdout.write("Done")
