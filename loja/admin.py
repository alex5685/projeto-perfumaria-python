# loja/admin.py
from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "preco_venda",
        "quantidade_estoque",
        "disponivel_no_site",
        "criado_em",
        "atualizado_em",
    )
    search_fields = ("nome",)
    list_filter = ("disponivel_no_site",)
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # ⚠️ Somente campos que existem no model Pedido
    list_display = ("id", "nome", "criado_em", "atualizado_em")
    search_fields = ("nome",)
    list_filter = ()
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    # ⚠️ Somente campos que existem em LogWhatsapps
    list_display = ("id", "pedido", "telefone", "status", "criado_em")
    search_fields = ("telefone", "mensagem", "status")
    list_filter = ("status",)
    readonly_fields = ("criado_em", "atualizado_em")
    # Para o popup/auto-complete do Pedido funcionar,
    # o PedidoAdmin precisa ter search_fields (já tem acima).
    autocomplete_fields = ("pedido",)
