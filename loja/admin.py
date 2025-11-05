from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps

# --- Produto (está funcionando; mantém uma configuração conservadora) ---
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco_venda", "quantidade_estoque", "disponivel_no_site")
    list_filter = ("disponivel_no_site",)
    search_fields = ("nome",)
    # só campos que certamente existem no seu model atual:
    readonly_fields = ("criado_em", "atualizado_em")

# --- Pedido: ZERADO para não quebrar ---
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """
    Admin minimalista e 100% seguro.
    NENHUM list_display/readonly_fields/ordering/date_hierarchy/etc.
    Deixa o Django montar o formulário e a changelist sozinho.
    """
    pass

# --- LogWhatsapps: configuração segura e mínima ---
@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    """
    Use só campos que existem. Caso tenha dúvidas, deixe 'pass'.
    """
    try:
        list_display = ("id", "created_at")
        readonly_fields = ("created_at",)
        ordering = ("-id",)
    except Exception:
        # Se por algum motivo não houver created_at, não arrisque.
        pass
