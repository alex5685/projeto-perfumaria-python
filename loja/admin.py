from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Campos que EXISTEM em Produto (conforme seu models/migrações atuais)
    list_display = (
        "id",
        "nome",
        "preco_venda",
        "quantidade_estoque",
        "disponivel_no_site",
        "criado_em",
        "atualizado_em",
    )
    list_filter = ("disponivel_no_site", "criado_em")
    search_fields = ("nome",)
    ordering = ("-criado_em",)
    date_hierarchy = "criado_em"
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """
    ATENÇÃO: Deixe apenas campos que existem no modelo Pedido.
    Pelo histórico, Pedido tem 'id' e 'criado_em'. 'atualizado_em' não existe nele.
    Se, futuramente, você adicionar mais campos ao Pedido, pode incluir aqui.
    """
    list_display = ("id", "criado_em")
    ordering = ("-criado_em",)
    date_hierarchy = "criado_em"
    readonly_fields = ("criado_em",)


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "mensagem_preview")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)

    def mensagem_preview(self, obj):
        # evita log gigante na listagem
        return (obj.mensagem or "")[:80]
    mensagem_preview.short_description = "Mensagem"
