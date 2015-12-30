from django.core.management.base import BaseCommand, CommandError
from django.apps import get_model
from library.models import *

import sys
sys.path.insert(0, '/home/ec2-user/JAV-scraper')

from DMM import DMM

class Command(BaseCommand):
    help = 'Updates from the DMM website'

    def add_arguments(self, parser):
        parser.add_argument('article', type=str)
        parser.add_argument('id', nargs='+', type=int)

    def handle(self, *args, **options):

        def get_obj( article, a_id ):

            model = get_model( 'library', article )

            try:
                return model.objects.get(_id=a_id)
            except model.DoesNotExist:
                title = dmm.get_title( article, a_id )
                # self.stdout.write("New %s: %s (%s)" % (article, title, m_id))
                model_object = model(_id=a_id,name=title)
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

        article = options['article']

        if article != 'maker':
            self.stdout.write("Error: %s - Only maker is supported now" % article )
            return

        dmm = DMM()

        for a_id in options['id']:
            works_c = Video.objects.filter(**{ "%s__pk" % article : a_id }).count()
            n_works = dmm.get_count( 0, article, a_id )
            self.stdout.write("Getting %d/%d works from %s %s ..." %(works_c,n_works,article,a_id))

            retvals = dmm.get_works( 0, a_id, n_works - works_c, callback = import_video )
            self.stdout.write(' ,'.join( em for ec,em in retvals if ec ))
        
        self.stdout.write("Done")

        return
