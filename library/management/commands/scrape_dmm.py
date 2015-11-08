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
            if target == 'tags':
                self.stdout.write("Scraping tags from DMM...")

                switcher = {
                    'その他': Tag.MISC,
                    'プレイ': Tag.PLAY,
                    'ジャンル': Tag.GENRE,
                    'コスチューム': Tag.COSTUME,
                    'ＡＶ女優タイプ': Tag.ATYPE,
                   'シチュエーション': Tag.SITUATION,
                }

                for tag_id, info in dmm.get_tags().items():
                    try:
                        tag = Tag.objects.get(_id=tag_id)
                    except Tag.DoesNotExist:
                        tag = Tag(_id=tag_id, name=info[0], category=switcher[info[1]] )
                        tag.save()
                    except TypeError:
                        self.stdout.write("TypeError")
            else:
                self.stdout.write("Error: Scrape target '%s' not recognised" % target)

        self.stdout.write("Done")
