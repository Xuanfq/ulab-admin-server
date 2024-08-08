from django.apps import AppConfig


class NettraversalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nettraversal"

    def ready(self) -> None:
        pass
