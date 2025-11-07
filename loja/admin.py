from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
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
    list_display = ("id", "nome", "criado_em", "atualizado_em")
    search_fields = ("nome",)
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "telefone", "status", "criado_em")
    search_fields = ("telefone", "mensagem", "status")
    readonly_fields = ("criado_em", "atualizado_em")

    # importante:
    # isso muda o widget do campo FK "pedido" para um campo de busca por ID,
    # em vez daquele select carregando todos os pedidos + popup mágico.
    # resultado:
    # - menos carga no banco
    # - menos risco de erro 500 ao abrir o popup (que chamava /admin/loja/pedido/add/)
    raw_id_fields = ("pedido",)
