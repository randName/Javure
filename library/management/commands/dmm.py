from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from library.models import *

from DMM import DMM

class Command(BaseCommand):
    help = 'Scrape the DMM website'

    def add_arguments(self, parser):
        parser.add_argument( 'action', type=str )
        parser.add_argument( 'article', type=str )

        parser.add_argument( '-d', '--domain', default='digital/videoa', type=str )
        parser.add_argument( '-i', '--id', nargs='*', type=int )

    def handle(self, *args, **options):

        def get_obj( article, a_id ):
            model = apps.get_model( 'library', article )

            try:
                return model.objects.get(_id=a_id)
            except model.DoesNotExist:
                item = dmm.get_article( 'digital/videoa', article, a_id )
                model_object = model(_id=a_id,name=item['name'])
                if article == "actress": model_object.furi = item['furi']
                model_object.save()

                return model_object

        def import_video( v ):
            v_slicer = ( 'cid', 'pid', 'title', 'display_id', 'runtime', 'released_date' )

            try:
                video = Video.objects.get(pid=v['pid'])
            except Video.DoesNotExist:
                video = Video(**{ k: v[k] for k in v_slicer })

                if not video.display_id: return ( 1, v['pid'] )

                for a in ( 'maker', 'label', 'series' ):
                   if a in v: setattr(video, a, get_obj( a, v[a] ) )

                for k in v['keywords']: video.keywords.add( get_obj( 'keyword', k ) )
                for a in v['actresses']: video.actresses.add( get_obj( 'actress', a ) )

                video.save()

            return ( None, None )

        dmm = DMM()

        action = options['action']
        article = options['article']
        domain = options['domain']
        
        if action == 'scrape':

            if article == 'keyword':
                self.stdout.write("Scraping keywords... ", ending="")

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
                self.stdout.write( "Deleting works from %s %s... "  % ( article, a_id ), ending="" )
                Video.objects.filter(**{ "%s__pk" % article : a_id }).delete()

        elif action == 'update':

            if article != 'maker':
                self.stdout.write("Error: %s - Only maker is supported now" % article)
                return

            if not options['id']:
                self.stdout.write("Error: No IDs given")
                return

            for a_id in options['id']:
                works_c = Video.objects.filter(**{ "%s__pk" % article : a_id }).count()
                n_works = dmm.get_article( domain, article, a_id )['count']

                self.stdout.write( "Status: %d/%d works from %s %s" % ( works_c, n_works, article, a_id ) )

                rem = n_works - works_c

                if rem == 0:
                    self.stdout.write( "Nothing to do." )
                    return

                self.stdout.write( "Getting %d works..." % rem )
                retvals = dmm.get_works( domain, a_id, rem, callback=import_video )
                # self.stdout.write(' ,'.join( em for ec,em in retvals if ec ))

        self.stdout.write("Done")

        return
