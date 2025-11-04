from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps

# ---------------------------
# Produto
# ---------------------------
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
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)


# ---------------------------
# Pedido
# Campos válidos hoje: id, nome, criado_em, atualizado_em
# (removemos cliente/status/total/etc. nas migrações anteriores)
# ---------------------------
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "criado_em", "atualizado_em")
    search_fields = ("nome",)
    list_filter = ("criado_em",)
    readonly_fields = ("criado_em", "atualizado_em")
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)


# ---------------------------
# LogWhatsapps
# Garanta que o modelo se chama LogWhatsapps (no plural) e tem
# pelo menos: id, mensagem, criado_em
# ---------------------------
@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    list_display = ("id", "mensagem", "criado_em")
    search_fields = ("mensagem",)
    readonly_fields = ("criado_em",)
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)
