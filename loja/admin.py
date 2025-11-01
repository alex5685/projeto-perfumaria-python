from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Ajuste estes campos conforme seu models.py
    list_display = ("id", "nome", "preco", "ativo")
    search_fields = ("nome", "descricao")
    list_filter = ("ativo",)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "status", "criado_em")
    search_fields = ("cliente", "observacoes")
    list_filter = ("status", "criado_em")

@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    list_display = ("id", "numero", "status", "criado_em")
    search_fields = ("numero", "mensagem")
    list_filter = ("status", "criado_em")
