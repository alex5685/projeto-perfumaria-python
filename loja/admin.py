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
    )
    search_fields = ("nome",)
    list_filter = ("disponivel_no_site",)
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "criado_em",
    )
    search_fields = ("nome",)
    readonly_fields = ("criado_em", "atualizado_em")
    # nada de date_hierarchy por enquanto


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pedido",
        "mensagem",
        "criado_em",
    )
    search_fields = ("mensagem",)
    readonly_fields = ("criado_em",)
    # nada de ordering que aponte pra campo que não existe
