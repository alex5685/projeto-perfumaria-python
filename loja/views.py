from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings

# Se você já tiver outras views, pode manter normalmente.
# Estes dois endpoints são só para diagnóstico e não interferem no admin.


@require_GET
def diag_ping(request):
    """
    Endpoint de vida simples.
    Útil para confirmar que a app está carregando sem quebrar na importação.
    """
    return JsonResponse({"ok": True, "debug": settings.DEBUG})


@require_GET
def diag_db(request):
    """
    Endpoint que força o ORM a tocar as três tabelas.
    Se houver problema de schema (coluna/tabela inexistente), vai retornar 500
    e o traceback ficará claro no log do Render.
    """
    from loja.models import Produto, Pedido, LogWhatsapps

    return JsonResponse(
        {
            "produto_count": Produto.objects.count(),
            "pedido_count": Pedido.objects.count(),
            "logwhatsapps_count": LogWhatsapps.objects.count(),
        }
    )
