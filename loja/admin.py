from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapp


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco", "estoque", "publicado")
    search_fields = ("nome",)
    list_filter = ("publicado", "estoque")
    ordering = ("-id",)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Corrigido: 'criado_em' -> 'data_pedido' (conforme models.py)
    list_display = ("id", "usuario", "status", "data_pedido", "total")
    list_filter = ("status", "data_pedido")
    search_fields = ("usuario__username",)
    readonly_fields = ("data_pedido",)
    date_hierarchy = "data_pedido"
    ordering = ("-data_pedido",)


@admin.register(LogWhatsapp)
class LogWhatsappAdmin(admin.ModelAdmin):
    # Corrigido: 'created_at' -> 'data_envio' (conforme models.py)
    list_display = ("id", "produto", "data_envio", "sucesso")
    list_filter = ("sucesso", "data_envio")
    search_fields = ("produto__nome",)
    date_hierarchy = "data_envio"
    ordering = ("-data_envio",)
