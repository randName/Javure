from django.core.management.base import BaseCommand, CommandError
from library.models import *

import sys
sys.path.insert(0, '/home/ec2-user/JAV-scraper')

from DMM import DMM

class Command(BaseCommand):
    help = 'Scrapes the DMM website'

    def add_arguments(self, parser):
        parser.add_argument('article', type=str)
        parser.add_argument('id', nargs='+', type=int)

    def handle(self, *args, **options):

        def get_model( article, m_id ):

            prop = {
                'maker': Maker, 'label': Label, 'series': Series,
                'director': Director, 'actress': Actress, 'keyword': Tag
            }

            model = prop[article]

            try:
                return model.objects.get(_id=m_id)
            except model.DoesNotExist:
                title = dmm.get_title( article, m_id )
                self.stdout.write("New %s: %s (%s)" % (article, title, m_id))
                model_object = model(_id=m_id,name=title)

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
                   if a in v: setattr(video, a, get_model( a, v[a] ) )

                for t in v['tags']: video.tags.add( get_model( 'keyword', t ) )
                for a in v['actresses']: video.actresses.add( get_model( 'actress', a ) )

                video.save()

            return ( None, None )

        article = options['article']

        if article != 'maker':
            self.stdout.write("Error: %s Only maker is supported now" % (article,))
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
