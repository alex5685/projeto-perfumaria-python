# loja/admin.py
from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Estes campos existem no Produto (conforme você já validou no shell):
    # ['id', 'nome', 'descricao_detalhada', 'preco_venda', 'quantidade_estoque',
    #  'imagem', 'disponivel_no_site', 'criado_em', 'atualizado_em']
    list_display = (
        "id",
        "nome",
        "preco_venda",
        "quantidade_estoque",
        "disponivel_no_site",
        "criado_em",
        "atualizado_em",
    )
    list_filter = ("disponivel_no_site",)
    search_fields = ("nome",)
    readonly_fields = ("criado_em", "atualizado_em")
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Para parar o erro de campos inexistentes no Pedido,
    # deixamos uma configuração mínima e 100% segura.
    # Se quiser mostrar mais colunas depois, me diga os nomes exatos
    # que estão em loja.models.Pedido e eu adiciono.
    list_display = ("id",)
    ordering = ("-id",)
    # Nada de readonly_fields/date_hierarchy/list_filter com campos não confirmados


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    # Idem: configuração mínima segura até confirmarmos os campos existentes.
    list_display = ("id",)
    ordering = ("-id",)
