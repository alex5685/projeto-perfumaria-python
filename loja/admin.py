from django.contrib import admin
from .models import Produto, Pedido, LogWhatsapps

# Admin "cru": sem ModelAdmin, sem list_display, sem inlines, etc.
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(LogWhatsapps)
