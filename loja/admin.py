# loja/admin.py
from django.contrib import admin

from .models import Produto, Pedido

# Tenta importar o modelo de log com os dois nomes possíveis.
LogWhatsappModel = None
try:
    # plural
    from .models import LogWhatsapps as LogWhatsappModel  # type: ignore
except Exception:
    try:
        # singular
        from .models import LogWhatsapp as LogWhatsappModel  # type: ignore
    except Exception:
        LogWhatsappModel = None


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Somente campos que existem e já foram validados
    list_display = ("id", "nome", "preco_venda", "disponivel_no_site")
    # Nada de callables ou campos inexistentes
    search_fields = ("nome",)
    list_filter = ("disponivel_no_site",)
    ordering = ("id",)
    readonly_fields = ()
    date_hierarchy = None


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Modo seguro: só 'id' até estabilizarmos os campos
    list_display = ("id",)
    search_fields = ()
    list_filter = ()
    ordering = ("id",)
    readonly_fields = ()
    date_hierarchy = None


if LogWhatsappModel:
    # Registro condicional conforme o nome real do modelo
    class _LogWhatsappsAdmin(admin.ModelAdmin):
        list_display = ("id",)
        search_fields = ()
        list_filter = ()
        ordering = ("id",)
        readonly_fields = ()
        date_hierarchy = None

    admin.site.register(LogWhatsappModel, _LogWhatsappsAdmin)
