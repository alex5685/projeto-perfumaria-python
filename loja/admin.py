# loja/admin.py
from django.contrib import admin
from django.utils.html import format_html

from .models import Produto, Pedido, LogWhatsapps


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Campos que existem de fato no modelo Produto
    list_display = (
        "id",
        "nome",
        "preco_venda",
        "quantidade_estoque",
        "disponivel_no_site",
        "criado_em",
        "atualizado_em",
        "preview_imagem",
    )
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_filter = ("disponivel_no_site",)
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)

    readonly_fields = ("criado_em", "atualizado_em", "preview_imagem")

    fieldsets = (
        ("Informações do Produto", {
            "fields": ("nome", "descricao_detalhada", "imagem", "preview_imagem")
        }),
        ("Comercial/Estoque", {
            "fields": ("preco_venda", "quantidade_estoque", "disponivel_no_site")
        }),
        ("Auditoria", {
            "fields": ("criado_em", "atualizado_em")
        }),
    )

    def preview_imagem(self, obj):
        """Pequena prévia da imagem (se existir)."""
        if obj.imagem:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;" />',
                obj.imagem.url,
            )
        return "—"
    preview_imagem.short_description = "Prévia"


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # CUIDADO: o modelo atual de Pedido só tem 'criado_em'
    list_display = ("id", "criado_em")
    list_display_links = ("id",)
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)
    readonly_fields = ("criado_em",)

    fieldsets = (
        ("Pedido", {"fields": ("criado_em",)}),
    )


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    # Campos existentes: 'mensagem' e 'criado_em'
    list_display = ("id", "mensagem_resumida", "criado_em")
    list_display_links = ("id",)
    search_fields = ("mensagem",)
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)
    readonly_fields = ("criado_em",)

    fieldsets = (
        ("Log de WhatsApp", {"fields": ("mensagem", "criado_em")}),
    )

    def mensagem_resumida(self, obj):
        txt = (obj.mensagem or "").strip()
        return (txt[:80] + "…") if len(txt) > 80 else (txt or "—")
    mensagem_resumida.short_description = "Mensagem"
