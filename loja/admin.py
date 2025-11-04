from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Produto, Pedido
# ⚠️ Por enquanto NÃO registramos LogWhatsapps para não quebrar o admin
# from .models import LogWhatsapps


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """
    Alinhado ao models atual:
      - nome
      - descricao_detalhada
      - preco_venda (DecimalField)
      - quantidade_estoque (IntegerField)
      - disponivel_no_site (BooleanField)
      - imagem (ImageField upload_to="produtos/")
      - criado_em / atualizado_em (DateTimeField auto_*)
    """
    list_display = (
        "id",
        "nome",
        "preco_venda",
        "quantidade_estoque",
        "disponivel_no_site",
        "criado_em",
        "atualizado_em",
    )
    list_filter = ("disponivel_no_site", "criado_em")
    search_fields = ("nome", "descricao_detalhada")
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)

    readonly_fields = ("criado_em", "atualizado_em", "imagem_preview")

    # Define explicitamente os campos que aparecem no form de edição
    fields = (
        "nome",
        "descricao_detalhada",
        "preco_venda",
        "quantidade_estoque",
        "disponivel_no_site",
        "imagem",
        "imagem_preview",
        "criado_em",
        "atualizado_em",
    )

    def imagem_preview(self, obj):
        if getattr(obj, "imagem", None):
            try:
                url = obj.imagem.url
            except Exception:
                return "—"
            return mark_safe(f'<img src="{url}" style="max-height:120px;max-width:100%%" />')
        return "—"

    imagem_preview.short_description = "Pré-visualização"


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """
    Alinhe aqui aos campos reais do seu Pedido.
    Este exemplo usa apenas campos estáveis para não quebrar o admin.
    """
    list_display = ("id", "criado_em")
    date_hierarchy = "criado_em"
    ordering = ("-criado_em",)
    readonly_fields = ("criado_em",)

    # Se você tiver outros campos (cliente, status etc.), adicione-os aqui,
    # sempre com os nomes EXATOS do models.py.
    fields = ("criado_em",)
