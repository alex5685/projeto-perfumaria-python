# loja/admin.py
from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapp


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco", "estoque")
    search_fields = ("nome",)
    list_filter = ("estoque",)
    ordering = ("-id",)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Campos que EXISTEM em loja.Pedido (confere no models.py)
    list_display = ("id", "cliente", "status", "criado_em")
    list_filter = ("status", "criado_em")   # >>> criado_em (não created_at)
    search_fields = ("cliente", "telefone", "endereco")
    readonly_fields = ("criado_em",)
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)


@admin.register(LogWhatsapp)
class LogWhatsappAdmin(admin.ModelAdmin):
    list_display = ("id", "produto", "data_envio", "sucesso")
    list_filter = ("sucesso", "data_envio")  # >>> data_envio (não created_at)
    search_fields = ("produto__nome",)
    date_hierarchy = "data_envio"
    ordering = ("-data_envio",)
