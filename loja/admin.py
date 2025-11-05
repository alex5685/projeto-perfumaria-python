# loja/admin.py

from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps

# -------------------------------------------------------------------
# MODO NUCLEAR (estável): registra os modelos sem qualquer ModelAdmin
# -------------------------------------------------------------------
# Isso evita erros causados por list_display / readonly_fields /
# ordering / date_hierarchy / inlines / filtros etc.
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(LogWhatsapps)

# ===================================================================
# OPCIONAL (descomente por etapas DEPOIS que o nuclear estiver ok)
# ===================================================================
# 1) Reintroduza um admin simples para Pedido
#
# @admin.register(Pedido)
# class PedidoAdmin(admin.ModelAdmin):
#     list_display = ("id", "nome", "criado_em", "atualizado_em")
#     search_fields = ("nome",)
#     ordering = ("-criado_em",)
#     readonly_fields = ("criado_em", "atualizado_em")
#
# 2) Reintroduza um admin simples para Produto
#
# @admin.register(Produto)
# class ProdutoAdmin(admin.ModelAdmin):
#     list_display = ("id", "nome", "preco_venda", "disponivel_no_site", "criado_em")
#     list_filter = ("disponivel_no_site",)
#     search_fields = ("nome",)
#     ordering = ("-criado_em",)
#     readonly_fields = ("criado_em", "atualizado_em")
#
# 3) Reintroduza um admin simples para LogWhatsapps
#
# @admin.register(LogWhatsapps)
# class LogWhatsappsAdmin(admin.ModelAdmin):
#     list_display = ("id", "pedido", "telefone", "status", "criado_em")
#     search_fields = ("telefone", "status", "mensagem")
#     ordering = ("-criado_em",)
#     # Se a tela carregar mas ficar lenta, pode usar raw_id_fields:
#     # raw_id_fields = ("pedido",)
#     readonly_fields = ("criado_em", "atualizado_em")
