from django.apps import AppConfig

class LojaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "loja"

    def ready(self):
        # IMPORTANTE: não carregue signals por enquanto.
        # from . import signals  # deixe comentado para isolar o 500 do admin
        return
