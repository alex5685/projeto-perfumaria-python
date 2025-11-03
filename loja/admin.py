# loja/admin.py
from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapp

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "disponivel_no_site")
    search_fields = ("nome",)
    list_filter = ("disponivel_no_site",)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "criado_em")

@admin.register(LogWhatsapp)
class LogWhatsappAdmin(admin.ModelAdmin):
    list_display = ("id", "criado_em")
