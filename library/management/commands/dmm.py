from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError
from django.db.models import Count
from django.apps import apps
from library.models import *

from javscraper.websites.DMM import *
from javscraper.japanese import MORAS

class Command(BaseCommand):
    help = 'Scrape the DMM website'

    def add_arguments(self, parser):
        parser.add_argument( 'action', type=str )
        parser.add_argument( 'article', type=str )

        parser.add_argument( '-r', '--realm', default=0, type=int )
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
                item = get_article(article, a_id)
                model_object = model(_id=a_id,name=item['name'])

                if article == "actress":
                    model_object.furi = item.get('furi', '')
                    model_object.alias = item.get('alias', '')

                try:
                    model_object.save()
                except DataError:
                    self.stdout.write("Error with %s" % item, ending='\n')

                return model_object

        def filled_articles(article):
            model = apps.get_model( 'library', article )
            a_list = model.objects.annotate(count=Count('video'))
            return tuple(a_list.filter(count__gt=0).values_list('pk',flat=True))

        def get_status(article, a_id, realm=0):
            works_l = Video.objects.filter(**{"%s__pk" % article: a_id})
            works_l = works_l.filter(content__realm=realm)
            # cont_l = Content.objects.filter(realm=realm)
            # cont_l = cont_l.filter(**{"video__%s__pk" % article: a_id})
            return works_l.count(), get_article(article, a_id, realm)['count']

        def new_content(v):
            try:
                content = Content.objects.get(cid=v['cid'])
                return False
            except Content.DoesNotExist:
                pass

            content = Content(**v)
            for k in get_related(v['cid'], v['realm']):
                try:
                    ct = Content.objects.get(cid=k[0])
                    content.video = ct.video
                    content.save()
                    return
                except Content.DoesNotExist:
                    pass

            return content

        def import_video(content, v):
            self.stdout.write('{:<20}'.format(v['cid']), ending='')

            v = get_video(v['cid'], v['realm'])

            if not v:
                self.stdout.write("Not found")
                return
            if '6561' in v['keywords']:
                self.stdout.write("TK   ", ending='\r')
                return

            video = Video(title=v['title'])

            for p in ('runtime', 'released_date'):
                if p in v: setattr(video, p, v[p])
            for a in ('maker', 'label', 'series', 'director'):
                if a in v: setattr(video, a, get_obj(a, v[a]))
            video.save()

            for k in v['keywords']: video.keywords.add(get_obj('keyword', k))
            for a in v['actresses']: video.actresses.add(get_obj('actress', a))
            video.save()

            self.stdout.write( "-> OK", ending='\r' )
            content.video = video
            content.save()

        article = options['article']
        action = options['action']
        start = options['start']
        realm = options['realm']
        
        if action == 'scrape':

            if article == 'keyword':
                self.stdout.write("Scraping keywords... ", ending="")
                for k in get_keywords():
                    k['category'] = int(k['category'])
                    get_obj('keyword',k)

            elif article == 'maker':
                self.stdout.write("Scraping makers...")
                for mora in MORAS:
                    self.stdout.write( mora, ending="\r" )
                    for m in get_makers(mora): get_obj('maker', m)
            else:
                self.stdout.write( "Error: Scrape article '%s' not recognised" % article )
                return

        elif action == 'reset':

            if not options['id']:
                self.stdout.write("Error: Clearing everything not supported yet")
                # Video.objects.all().delete()

                # Label.objects.annotate(vc=Count('video')).filter(vc=0).delete()
                return

            for a_id in options['id']:
                self.stdout.write("Deleting works from %s %s... "  % (article, a_id), ending="")
                Video.objects.filter(**{"%s__pk" % article: a_id}).delete()
                return

        elif action == 'status':

            if not options['id']:
                options['id'] = filled_articles(article)

            for a_id in options['id']:
                hv, tt = get_status(article, a_id, realm)
                if tt == 0: continue
                self.stdout.write("%s %5s: " % (article, a_id), ending="")
                self.stdout.write("%d/%d \t %s" % (hv, tt, "Ok" if hv >= tt else (tt-hv)))

        elif action == 'update':

            if not options['id']:
                self.stdout.write("Updating all later.")
                return

            for a_id in options['id']:
                have, avail = get_status(article, a_id, realm)
                rem = avail - have
                if rem < 10:
                    self.stdout.write( "%s remaining, not bothering" % rem )
                    continue

                self.stdout.write( "Status: %d/%d from %s %s" % (have, avail, article, a_id) )
                self.stdout.write( "Getting %d works from page %d..." % (rem, start) )
                for v in get_article_list(article, a_id, realm=realm, start=start, count=rem):
                    if new_content(v): import_video(v)
                self.stdout.write( "\n" )

        elif action == 'fill':

            if not options['id']:
                self.stdout.write("Cannot fill all.")
                return

            for a_id in options['id']:
                have, avail = get_status(article, a_id, realm)

                self.stdout.write( "Status: %d/%d from %s %s" % (have, avail, article, a_id) )
                for v in get_article_list(article, a_id, realm=realm, start=start, count=avail):
                    c = new_content(v)
                    if c: import_video(c, v)
                self.stdout.write( "\n" )

        elif action == 'name':

            if not options['id']:
                self.stdout.write("Naming all.")
                options['id'] = filled_articles(article)

            for a_id in options['id']:
                for v in Video.objects.filter(**{"%s__pk" % article: a_id}):
                    if v.name: continue
                    pid = v.content_set.first().pid
                    self.stdout.write('{:<20}'.format(pid), ending='')
                    lb = v.label.pk if v.label else 0
                    v.name = get_name({ 'pid': pid, 'maker': v.maker.pk, 'label': lb})
                    self.stdout.write( '-> {:<15}'.format(v.name), ending='\r' )
                    v.save()
                self.stdout.write( "\n" )

        self.stdout.write("Done")
