from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapp # Importa os modelos que você acabou de criar

# Registra o modelo Produto no painel ADM (Controle de Estoque e Publicação)
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'publicado', 'data_criacao')
    list_filter = ('publicado', 'data_criacao')
    search_fields = ('nome', 'descricao')
    list_editable = ('preco', 'estoque', 'publicado') # Edição rápida na lista

# Registra o modelo Pedido no painel ADM (Acompanhamento de Vendas)
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'data_pedido', 'total', 'status')
    list_filter = ('status', 'data_pedido')
    search_fields = ('id', 'usuario__username')

# Registra o Log do WhatsApp
admin.site.register(LogWhatsapp)

