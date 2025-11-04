from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps

# Utilitário: garante que só usamos campos que realmente existem
def only_existing(model, names):
    valid = {f.name for f in model._meta.get_fields() if hasattr(f, "name")}
    return [n for n in names if n in valid]

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Campos esperados no modelo atual:
    # nome, descricao_detalhada, imagem, quantidade_estoque,
    # preco_venda, disponivel_no_site, criado_em, atualizado_em
    list_display  = only_existing(Produto, [
        "nome", "preco_venda", "quantidade_estoque",
        "disponivel_no_site", "criado_em", "atualizado_em",
    ])
    list_filter   = only_existing(Produto, [
        "disponivel_no_site", "criado_em", "atualizado_em",
    ])
    search_fields = only_existing(Produto, ["nome"])
    date_hierarchy = "criado_em" if "criado_em" in {f.name for f in Produto._meta.get_fields()} else None
    ordering      = ["-criado_em"] if "criado_em" in {f.name for f in Produto._meta.get_fields()} else None
    readonly_fields = only_existing(Produto, ["criado_em", "atualizado_em"])


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Campos esperados no modelo atual do Pedido:
    # cliente (se existir), criado_em, atualizado_em, etc.
    # Use apenas os existentes aí no seu models.py
    base = {f.name for f in Pedido._meta.get_fields()}
    # linhas, filtros, busca e ordenação só com campos válidos
    list_display  = only_existing(Pedido, [
        "id", "cliente", "criado_em", "atualizado_em",
    ]) or ["id"]
    list_filter   = only_existing(Pedido, ["criado_em", "atualizado_em"])
    search_fields = only_existing(Pedido, ["cliente"])
    date_hierarchy = "criado_em" if "criado_em" in base else None
    ordering       = ["-criado_em"] if "criado_em" in base else ["-id"]
    readonly_fields = only_existing(Pedido, ["criado_em", "atualizado_em"])


@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(admin.ModelAdmin):
    # Ajuste estes nomes de acordo com o seu LogWhatsapps atual
    # (ex.: telefone, mensagem, criado_em, status…)
    list_display  = only_existing(LogWhatsapps, [
        "id", "telefone", "mensagem", "criado_em",
    ]) or ["id"]
    list_filter   = only_existing(LogWhatsapps, ["criado_em"])
    search_fields = only_existing(LogWhatsapps, ["telefone", "mensagem"])
    date_hierarchy = "criado_em" if "criado_em" in {f.name for f in LogWhatsapps._meta.get_fields()} else None
    ordering       = ["-criado_em"] if "criado_em" in {f.name for f in LogWhatsapps._meta.get_fields()} else ["-id"]
    readonly_fields = only_existing(LogWhatsapps, ["criado_em"])
