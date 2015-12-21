from django.core.management.base import BaseCommand, CommandError
from library.models import *

import sys, itertools
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

        def get_model( article, m_id ):

            prop = {
                'maker': Maker,
                'label': Label,
                'keyword': Tag,
                'series': Series,
                'actress': Actress,
                'director': Director
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

        article = options['article']

        # spinner = itertools.cycle(['-', '/', '|', '\\'])

        if article != 'maker':
            self.stdout.write("Error: %s Only maker is supported now" % (article,))
            return

        for a_id in options['id']:
            kwa = { article: get_model( article, a_id ) }
            works_c = Video.objects.filter(**kwa).count()
            n_works = dmm.get_count( 0, article, a_id )
            self.stdout.write("Getting %d/%d works from %s %s ..." % (works_c,n_works,article,a_id))

            for v in dmm.get_works( 0, a_id, n_works ):
                # self.stdout.write( "\b" )
                # self.stdout.write( spinner.next(), ending="" )
                # self.stdout.flush()

                try:
                    video = Video.objects.get(cid=v['cid'])
                except Video.DoesNotExist:
                    video = Video(cid=v['cid'],title=v['title'],released_date=v['date'])
                    video.runtime = timedelta(minutes=v['runtime'])

                    video.display_id = dmm.rename( v['cid'], v['maker'] )

                    if not video.display_id: continue

                    video.maker = get_model( 'maker', v['maker'] )

                    for a in v['actresses']:
                        video.actresses.add( get_model( 'actress', a ) )

                    for t in v['tags']:
                        video.tags.add( get_model( 'keyword', t ) )

                    if 'director' in v:
                        video.director = get_model( 'director', v['director'] )

                    if 'label' in v:
                        video.label = get_model( 'label', v['label'] )

                    if 'series' in v:
                        video.series = get_model( 'series', v['series'] )

                    video.save()

        self.stdout.write("Done")

        return

