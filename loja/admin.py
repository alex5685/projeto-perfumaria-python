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
    list_filter = ("disponivel_no_site",)
    search_fields = ("nome",)
    readonly_fields = ("criado_em", "atualizado_em")
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Atenção: usar os NOMES REAIS dos campos (criado_em/atualizado_em), não created_at/updated_at.
    list_display = ("id", "nome", "criado_em", "atualizado_em")
    search_fields = ("nome",)
    readonly_fields = ("criado_em", "atualizado_em")
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    # Campos existentes no modelo:
    # pedido (FK opcional), telefone, mensagem, status, criado_em, atualizado_em
    list_display = ("id", "pedido", "telefone", "status", "criado_em", "atualizado_em")
    list_filter = ("status",)
    search_fields = ("telefone", "mensagem", "status")
    readonly_fields = ("criado_em", "atualizado_em")
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)
