import os.path

from django.conf import settings
from django.core.management.commands.loaddata import Command as LoadCommand
from django.db import DEFAULT_DB_ALIAS

from system.models import *
from server.settings import LANGUAGE_CODE


class Command(LoadCommand):
    help = 'init data'
    model_names = [UserRole, DeptInfo, Menu, MenuMeta, SystemConfig, DataPermission, FieldPermission, ModelLabelField]
    missing_args_message = None
    language_choices = ['en', 'zh', 'default']

    def add_arguments(self, parser):
        parser.add_argument(
            "-m",
            "--mode",
            action = "store",
            dest = "mode",
            choices = self.language_choices,
            help = "set data mode",
            default = LANGUAGE_CODE if LANGUAGE_CODE in self.language_choices else 'default')

    def handle(self, *args, **options):
        fixture_labels = []
        mode = options["mode"]
        file_root = os.path.join(settings.BASE_DIR, f"config/init/database/{mode}")
        for model in self.model_names:
            fixture_labels.append(os.path.join(file_root, f"{model._meta.model_name}.json"))
        options["ignore"] = ""
        options["database"] = DEFAULT_DB_ALIAS
        options["app_label"] = ""
        options["exclude"] = []
        options["format"] = "json"
        super(Command, self).handle(*fixture_labels, **options)
