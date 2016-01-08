from django.core.management.base import BaseCommand, CommandError
from library.models import *

import sys
sys.path.insert(0, '/home/ec2-user/JAV-scraper')

from DMM import DMM

class Command(BaseCommand):
    help = 'Scrape the DMM website'

    def add_arguments(self, parser):
        parser.add_argument( 'action', type=str )
        parser.add_argument( 'article', type=str )

        parser.add_argument( '-d', '--domain', default='digital/videoa', type=str )
        parser.add_argument( '-i', '--id', nargs='*', type=int )

    def handle(self, *args, **options):

        dmm = DMM()

        action = options['action']
        article = options['article']
        domain = options['domain']
        
        if action == 'scrape':

            if article == 'keyword':
                self.stdout.write("Scraping keywords...", ending="")

                for k in dmm.get_keywords(): Keyword.objects.get_or_create(**k)

            elif article == 'maker':
                self.stdout.write("Scraping makers...")

                for mora in dmm.MORAS:
                    self.stdout.write( mora, ending="\r" )
                    dmm.get_makers( mora, callback=lambda x: Maker.objects.get_or_create(**x) )

            elif article == 'actress':
                self.stdout.write("Scraping actresses...")

                for mora in dmm.MORAS:
                    self.stdout.write( mora, ending="\r" )
                    dmm.get_actresses( mora, callback=lambda x: Actress.objects.get_or_create(**x) )

            else:
                self.stdout.write( "Error: Scrape article '%s' not recognised" % target )
                return

        elif action == 'reset':

            if article != 'maker':
                self.stdout.write("Error: %s - Only maker is supported now" % article)
                return

            if not options['id']:
                self.stdout.write("Error: Clearing everything not supported yet")
                return

            for a_id in options['id']:
                self.stdout.write( "Deleting works from %s %s ..."  % ( article, a_id ) )
                Video.objects.filter(**{ "%s__pk" % article : a_id }).delete()

        self.stdout.write("Done")
