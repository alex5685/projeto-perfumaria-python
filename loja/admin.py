from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco_venda", "quantidade_estoque",
                    "disponivel_no_site", "criado_em", "atualizado_em")
    search_fields = ("nome",)
    list_filter = ("disponivel_no_site",)
    ordering = ("-criado_em",)
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "criado_em", "atualizado_em")
    search_fields = ("nome",)
    ordering = ("-criado_em",)
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "telefone", "status", "criado_em", "atualizado_em")
    search_fields = ("telefone", "mensagem", "status")
    list_filter = ("status",)
    ordering = ("-criado_em",)
    readonly_fields = ("criado_em", "atualizado_em")
