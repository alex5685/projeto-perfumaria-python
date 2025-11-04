from django.contrib import admin
from .models import Produto, Pedido

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco_venda", "quantidade_estoque", "disponivel_no_site", "criado_em")
    list_filter = ("disponivel_no_site",)
    search_fields = ("nome", "descricao_detalhada")
    readonly_fields = ("criado_em", "atualizado_em")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Deixe BEM simples até validarmos os campos existentes:
    list_display = ("id", "criado_em", "atualizado_em")
    readonly_fields = ("criado_em", "atualizado_em")

    # Remova QUALQUER coisa que referencie campos que não existem mais:
    # nada de ordering, list_filter, date_hierarchy, search_fields com
    # campos antigos (status, cliente, total, etc.).
