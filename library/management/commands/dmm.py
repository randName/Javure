from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError
from django.db.models import Count
from django.apps import apps
from library.models import *

from DMM import DMM

class Command(BaseCommand):
    help = 'Scrape the DMM website'

    def add_arguments(self, parser):
        parser.add_argument( 'action', type=str )
        parser.add_argument( 'article', type=str )

        parser.add_argument( '-s', '--start', default=1, type=int )
        parser.add_argument( '-i', '--id', nargs='*', type=int )

    def handle(self, *args, **options):

        def get_obj( article, a_id ):
            model = apps.get_model( 'library', article )

            if a_id is None: return

            if isinstance(a_id, dict):
                return model.objects.get_or_create(**a_id)

            try:
                return model.objects.get(_id=a_id)
            except model.DoesNotExist:
                item = dmm.get_article( 0, article, a_id )
                model_object = model(_id=a_id,name=item['name'])
                if article == "actress":
                    model_object.furi = item.get( 'furi', '' )
                    model_object.alias = item.get( 'alias', '' )
                try:
                    model_object.save()
                except DataError:
                    print( item )

                return model_object

        def import_video( v ):
            v_slicer = ( '_id', 'title', 'runtime', 'released_date' )

            if not v['_id']: return ( 1, v['cid'] )

            try:
                video = Video.objects.get(_id=v['_id'])
            except Video.DoesNotExist:
                video = Video(**{ k: v[k] for k in v_slicer })

                for a in ( 'maker', 'label', 'series' ):
                   if a in v: setattr(video, a, get_obj( a, v[a] ) )
                video.save()

                for k in v['keywords']: video.keywords.add( get_obj( 'keyword', k ) )
                for a in v['actresses']: video.actresses.add( get_obj( 'actress', a ) )

                video.save()

            try:
                content = Content.objects.get(cid=v['cid'])
            except Content.DoesNotExist:
                content = Content(**{ k: v[k] for k in ( 'cid', 'pid', 'realm' ) })
                content.video = video

                content.save()

            fix_video( video )

            return ( None, None )

        def fix_video( video ):

            self.stdout.write( "\r%s  \t" % video.pk, ending="" )

            c = video.content_set.first()
            w = dmm.get_work_page( c.realm, c.cid )

            video.released_date = w['date']

            d = 'director'
            if d in w: setattr( video, d, get_obj( d, w[d] ) )

            video.save()

        dmm = DMM()

        action = options['action']
        article = options['article']
        start = options['start']
        
        if action == 'scrape':

            if article == 'keyword':
                self.stdout.write("Scraping keywords... ", ending="")

                for k in dmm.get_keywords(): get_obj('keyword',k)

            elif article == 'maker':
                self.stdout.write("Scraping makers...")

                for mora in dmm.MORAS:
                    self.stdout.write( mora, ending="\r" )
                    dmm.get_makers( mora, callback=lambda x: get_obj('maker',x) )

            elif article == 'actress':
                self.stdout.write("Scraping actresses...")

                for mora in dmm.MORAS:
                    self.stdout.write( mora, ending="\r" )
                    dmm.get_actresses( mora, callback=lambda x: get_obj('actress',x) )

            else:
                self.stdout.write( "Error: Scrape article '%s' not recognised" % article )
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
                self.stdout.write("No IDs given, updating all")

                maker_list = Maker.objects.annotate(count=Count('video'))
                options['id'] = list( maker_list.filter(count__gt=0).values_list('pk',flat=True) )

            for a_id in options['id']:
                works_l = Video.objects.filter(**{ "%s__pk" % article : a_id })
                realm = works_l.first().content_set.first().realm
                works_c = works_l.count()

                n_works = dmm.get_article( realm, article, a_id )['count']

                self.stdout.write( "Status: %d/%d from %s %s" % (works_c,n_works,article,a_id) )

                rem = n_works - works_c

                if rem == 0:
                    self.stdout.write( "Nothing to do." )
                    continue

                self.stdout.write( "Getting %d works from page %d..." % ( rem, start ) )
                retvals = dmm.get_works( realm, a_id, rem, page=start, callback=import_video )
                # self.stdout.write(' ,'.join( em for ec,em in retvals if ec ))
                self.stdout.write( "\n" )

        elif action == 'fix':

            if not options['id']:
                self.stdout.write("Error: No IDs given")
                return

            for a_id in options['id']:
                self.stdout.write( "Fixing videos from %s %s... " %( article, a_id ) )

                for v in Video.objects.filter(**{ "%s__pk" % article : a_id }): fix_video( v )

                self.stdout.write( "\n" )

        self.stdout.write("Done")
