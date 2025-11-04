from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps


# ---------- Utilidades ----------
class SafeTimestampAdmin(admin.ModelAdmin):
    """
    Evita erros de system check quando um modelo não possui
    'criado_em' / 'atualizado_em'. Não define readonly_fields
    como atributo de classe; decide dinamicamente.
    """
    def get_readonly_fields(self, request, obj=None):
        ro = []
        # Checa no model, não no obj, para funcionar no changelist
        if hasattr(self.model, "criado_em"):
            ro.append("criado_em")
        if hasattr(self.model, "atualizado_em"):
            ro.append("atualizado_em")
        return tuple(ro)


# ---------- Produto ----------
@admin.register(Produto)
class ProdutoAdmin(SafeTimestampAdmin):
    list_display = (
        "id",
        "nome",
        # Estes campos existem em Produto
        "preco_venda",
        "quantidade_estoque",
        "disponivel_no_site",
    )
    list_filter = ("disponivel_no_site",)
    search_fields = ("nome",)

    # Em Produto nós TEMOS 'criado_em'; se quiser, também dá
    # para exibir no list_display adicionando "criado_em".
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)


# ---------- Pedido ----------
@admin.register(Pedido)
class PedidoAdmin(SafeTimestampAdmin):
    # Use apenas campos que você tem em Pedido.
    # Pelo histórico/migrações, 'atualizado_em' NÃO existe em Pedido.
    # Ajuste 'cliente' se o nome do campo for outro (ex.: 'nome_cliente').
    list_display = (
        "id",
        "cliente",       # troque aqui se o nome do campo for diferente
        "criado_em",
    )
    search_fields = ("cliente",)  # idem
    date_hierarchy = "criado_em"  # este existe em Pedido
    ordering = ("-criado_em",)    # idem


# ---------- LogWhatsapps ----------
@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(SafeTimestampAdmin):
    # Use o mínimo garantido. Acrescente outros depois que confirmar os nomes.
    list_display = ("id",) + (("criado_em",) if hasattr(LogWhatsapps, "criado_em") else ())
    search_fields = ()  # preencha depois (ex.: ("numero",))
    # Evite 'ordering' e 'date_hierarchy' aqui até confirmar os nomes dos campos
    # ordering = ("-criado_em",)
    # date_hierarchy = "criado_em"
