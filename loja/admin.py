# loja/admin.py
from django.contrib import admin
from .models import Produto, Pedido

# -------- Produto --------
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
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
    search_fields = ("nome", "descricao_detalhada")
    readonly_fields = ("criado_em", "atualizado_em")
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)

# -------- Pedido --------
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Mostre os timestamps; ajuste/complete depois com os campos de negócio que quiser
    list_display = ("id", "criado_em", "atualizado_em")
    readonly_fields = ("criado_em", "atualizado_em")
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)
    search_fields = ()  # preencha se houver campos de texto pesquisáveis
    list_filter = ()    # idem

# -------- LogWhatsapps (opcional/defensivo) --------
# Só registra se o modelo existir e tiver 'criado_em', evitando travar o system check.
try:
    from .models import LogWhatsapps  # type: ignore

    if hasattr(LogWhatsapps, "criado_em"):
        @admin.register(LogWhatsapps)
        class LogWhatsappsAdmin(admin.ModelAdmin):
            # ajuste os nomes conforme os campos reais do modelo
            base_fields = ["id", "criado_em"]
            if hasattr(LogWhatsapps, "telefone"):
                base_fields.insert(1, "telefone")
            if hasattr(LogWhatsapps, "mensagem"):
                base_fields.insert(2, "mensagem")

            list_display = tuple(base_fields)
            readonly_fields = ("criado_em",) + (("atualizado_em",) if hasattr(LogWhatsapps, "atualizado_em") else ())
            date_hierarchy = "criado_em"
            ordering = ("-criado_em",)
except Exception:
    # Se o import falhar ou os campos não existirem, simplesmente não registra para não quebrar o deploy.
    pass
