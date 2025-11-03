from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "disponivel_no_site")
    search_fields = ("nome",)
    list_filter = ("disponivel_no_site",)
