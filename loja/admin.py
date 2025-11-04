from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps

# utilitários ---------------------------------------------------------------

def field_names(model):
    """Retorna o conjunto de nomes de campos reais do modelo."""
    return {f.name for f in model._meta.get_fields()}

def keep_existing(model, names):
    """Mantém apenas os nomes que existem no model (ignora None/duplos)."""
    if not names:
        return []
    names = [n for n in names if n]  # remove None/strings vazias
    existing = field_names(model)
    out = []
    for n in names:
        base = n.lstrip("-")  # suporta ordenação com '-'
        if base in existing:
            out.append(n)
    # evita lista vazia em locais que precisam de ao menos 1 entrada
    return out

class SafeAdmin(admin.ModelAdmin):
    """
    ModelAdmin que só expõe campos existentes — evita falhas de system check
    (admin.E0xx) quando os modelos mudam e ainda não têm migrações aplicadas.
    """
    # candidatas (defina nas subclasses)
    list_display_candidates     = ()
    list_filter_candidates      = ()
    search_fields_candidates    = ()
    readonly_fields_candidates  = ()
    ordering_candidates         = ()
    date_hierarchy_candidate    = None

    # getters dinâmicos usados pelo Django e pelos system checks
    def get_list_display(self, request):
        values = keep_existing(self.model, self.list_display_candidates)
        # fallback amigável
        return tuple(values or ("id", "__str__"))

    def get_list_filter(self, request):
        return tuple(keep_existing(self.model, self.list_filter_candidates))

    def get_search_fields(self, request):
        return tuple(keep_existing(self.model, self.search_fields_candidates))

    def get_readonly_fields(self, request, obj=None):
        return tuple(keep_existing(self.model, self.readonly_fields_candidates))

    def get_ordering(self, request):
        return tuple(keep_existing(self.model, self.ordering_candidates))

    def get_date_hierarchy(self, request):
        cand = self.date_hierarchy_candidate
        if cand and cand in field_names(self.model):
            return cand
        return None

# Produto -------------------------------------------------------------------

@admin.register(Produto)
class ProdutoAdmin(SafeAdmin):
    list_display_candidates    = ("id", "nome", "preco_venda", "quantidade_estoque",
                                  "disponivel_no_site", "criado_em", "atualizado_em")
    list_filter_candidates     = ("disponivel_no_site",)
    search_fields_candidates   = ("nome", "descricao_detalhada")
    readonly_fields_candidates = ("criado_em", "atualizado_em")
    ordering_candidates        = ("-criado_em", "nome")
    date_hierarchy_candidate   = "criado_em"

# Pedido --------------------------------------------------------------------

@admin.register(Pedido)
class PedidoAdmin(SafeAdmin):
    # coloquei um conjunto amplo de candidatos; o mixin filtra os inexistentes
    list_display_candidates    = ("id", "cliente", "status", "total",
                                  "criado_em", "atualizado_em")
    list_filter_candidates     = ("status",)
    search_fields_candidates   = ("cliente", "email", "telefone")
    readonly_fields_candidates = ("criado_em", "atualizado_em")
    ordering_candidates        = ("-criado_em",)
    date_hierarchy_candidate   = "criado_em"

# LogWhatsapps --------------------------------------------------------------

@admin.register(LogWhatsapps)
class LogWhatsappsAdmin(SafeAdmin):
    list_display_candidates    = ("id", "pedido", "evento", "detalhes", "criado_em")
    list_filter_candidates     = ("evento",)
    search_fields_candidates   = ("pedido__id", "detalhes")
    readonly_fields_candidates = ("criado_em",)
    ordering_candidates        = ("-criado_em",)
    date_hierarchy_candidate   = "criado_em"
