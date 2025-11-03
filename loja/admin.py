from django.contrib import admin
from django.utils.html import format_html
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
    list_filter = ("disponivel_no_site", "criado_em")
    search_fields = ("nome",)
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)

    readonly_fields = ("criado_em", "atualizado_em", "imagem_preview")
    fields = (
        "nome",
        "descricao_detalhada",
        "preco_venda",
        "quantidade_estoque",
        "imagem",
        "imagem_preview",
        "disponivel_no_site",
        "criado_em",
        "atualizado_em",
    )

    def imagem_preview(self, obj):
        """
        Mostra um preview da imagem sem nunca derrubar o admin.
        Se não houver imagem ou a URL falhar (S3, credencial, permissão),
        retorna um texto amigável.
        """
        try:
            if obj.imagem and hasattr(obj.imagem, "url"):
                return format_html(
                    '<img src="{}" style="max-height:160px; border-radius:8px" />',
                    obj.imagem.url,
                )
        except Exception:
            return "(sem imagem / erro ao gerar URL)"
        return "(sem imagem)"

    imagem_preview.short_description = "Pré-visualização"


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "criado_em")
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    list_display = ("id", "criado_em")
    search_fields = ("mensagem",)
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)
