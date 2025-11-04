from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco_venda', 'quantidade_estoque', 'disponivel_no_site', 'criado_em', 'atualizado_em')
    list_filter = ('disponivel_no_site', 'criado_em', 'atualizado_em')
    search_fields = ('nome', 'descricao_detalhada')
    ordering = ('-criado_em',)
    date_hierarchy = 'criado_em'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'quantidade', 'criado_em')
    search_fields = ('produto__nome',)
    list_filter = ('criado_em',)
    ordering = ('-criado_em',)
    date_hierarchy = 'criado_em'


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    list_display = ('id', 'mensagem', 'enviado_em')
    search_fields = ('mensagem',)
    ordering = ('-enviado_em',)
    date_hierarchy = 'enviado_em'
