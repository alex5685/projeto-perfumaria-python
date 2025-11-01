from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapp  # <-- nome exato da classe no models.py

# Ajuste as colunas conforme os campos reais do seu models.py.
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco")  # troque pelos campos que existem aí
    search_fields = ("nome",)
    list_filter = ()

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "status", "criado_em")  # ajuste conforme o seu model
    search_fields = ("cliente",)
    list_filter = ("status",)

@admin.register(LogWhatsapp)
class LogWhatsappAdmin(admin.ModelAdmin):
    list_display = ("id", "numero", "mensagem", "created_at")  # ajuste conforme o seu model
    search_fields = ("numero", "mensagem")
    list_filter = ("created_at",)
