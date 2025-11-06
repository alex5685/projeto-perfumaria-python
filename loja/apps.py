from django.apps import AppConfig
import os

class LojaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "loja"

    def ready(self):
        # Carrega os signals só se a flag estiver ativa (padrão: DESLIGADO em produção para testarmos)
        if os.getenv("ENABLE_LOJA_SIGNALS", "0") == "1":
            try:
                from . import signals  # noqa: F401
            except Exception:
                # Não deixe um erro de import matar o admin
                import logging
                logging.exception("Falha ao carregar loja.signals")
