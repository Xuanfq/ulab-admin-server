from django.core.management.base import BaseCommand

from common.core.config import ConfigCacheBase


class Command(BaseCommand):
    help = 'Expire config caches'

    def add_arguments(self, parser):
        parser.add_argument('key', nargs='?', type=str, default='*')

    def handle(self, *args, **options):
        ConfigCacheBase().invalid_config_cache(options.get('key', '*'))
        ConfigCacheBase(px='user').invalid_config_cache(options.get('key', '*'))
