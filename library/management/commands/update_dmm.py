from django.core.management.base import BaseCommand, CommandError
from library.models import *

import sys
sys.path.insert(0, '/home/ec2-user/JAV-scraper')

from datetime import timedelta

from DMM import DMM

class Command(BaseCommand):
    help = 'Scrapes the DMM website'

    def add_arguments(self, parser):
        parser.add_argument('article', type=str)
        parser.add_argument('id', nargs='+', type=int)

    def handle(self, *args, **options):

        dmm = DMM()

        def get_model( model, article, m_id ):
            try:
                return model.objects.get(_id=m_id)
            except model.DoesNotExist:
                title = dmm.get_title( article, m_id )
                self.stdout.write("New %s: %s (%s)" % (article, title, m_id))
                model_object = model(_id=m_id,name=title)

                model_object.save()

                return model_object

        article = options['article']

        if article == 'maker':
            self.stdout.write("Getting maker")
        else:
            self.stdout.write("Error: %s Only maker is supported now" % (article,))
            return

        for a_id in options['id']:
            # num_works = dmm.get_count( 0, article, a_id )

            for v in dmm.get_works( 0, a_id, 5 ):
                try:
                    video = Video.objects.get(cid=v['cid'])
                except Video.DoesNotExist:
                    video = Video(cid=v['cid'],title=v['title'],released_date=v['date'])
                    video.runtime = timedelta(minutes=v['runtime'])

                    video.display_id = video.cid

                    video.maker = get_model( Maker, 'maker', v['maker'] )

                    for a in v['actresses']:
                        video.actresses.add( get_model( Actress, 'actress', a ) )

                    for t in v['tags']:
                        video.tags.add( get_model( Tag, 'keyword', t ) )

                    if 'director' in v:
                        video.director = get_model( Director, 'director', v['director'] )

                    if 'label' in v:
                        video.label = get_model( Label, 'label', v['label'] )

                    if 'series' in v:
                        video.series = get_model( Series, 'series', v['series'] )

                    # self.stdout.write( repr( v ) )
                
                    video.save()

        self.stdout.write("Done")

        return

