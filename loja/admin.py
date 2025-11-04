from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps


def _has_field(model, name: str) -> bool:
    return name in {f.name for f in model._meta.fields}


def _pick(model, *names):
    existing = {f.name for f in model._meta.fields}
    return tuple(n for n in names if n in existing)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Exibe apenas campos que existem no modelo
    list_display = _pick(
        Produto,
        "id",
        "nome",
        "preco_venda",
        "quantidade_estoque",
        "disponivel_no_site",
        "criado_em",
        "atualizado_em",
    )
    search_fields = _pick(Produto, "nome", "descricao_detalhada")
    list_filter = _pick(Produto, "disponivel_no_site", "criado_em", "atualizado_em")
    readonly_fields = _pick(Produto, "criado_em", "atualizado_em")

    # Define date_hierarchy somente se o campo existir
    if _has_field(Produto, "criado_em"):
        date_hierarchy = "criado_em"

    ordering = ("-id",) if _has_field(Produto, "id") else None


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Coloque aqui o superset de campos “possíveis” do seu Pedido;
    # o helper _pick garante que só os existentes serão usados.
    list_display = _pick(
        Pedido,
        "id",
        "cliente",           # será ignorado se não existir
        "status",
        "total",
        "criado_em",
        "atualizado_em",
    )
    search_fields = _pick(Pedido, "cliente", "email", "telefone")
    list_filter = _pick(Pedido, "status", "criado_em", "atualizado_em")
    readonly_fields = _pick(Pedido, "criado_em", "atualizado_em")

    if _has_field(Pedido, "criado_em"):
        date_hierarchy = "criado_em"

    ordering = ("-id",) if _has_field(Pedido, "id") else None


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    list_display = _pick(
        LogWhatsapps,
        "id",
        "pedido",        # se tiver FK para Pedido
        "mensagem",
        "criado_em",
        "atualizado_em",
    )
    search_fields = _pick(LogWhatsapps, "mensagem")
    list_filter = _pick(LogWhatsapps, "criado_em", "atualizado_em")
    readonly_fields = _pick(LogWhatsapps, "criado_em", "atualizado_em")

    if _has_field(LogWhatsapps, "criado_em"):
        date_hierarchy = "criado_em"

    ordering = ("-id",) if _has_field(LogWhatsapps, "id") else None
