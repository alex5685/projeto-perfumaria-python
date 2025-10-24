# loja/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Rotas Públicas (Frontend)
    path('', views.home, name='home'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/<int:produto_id>/', views.detalhe_produto, name='detalhe_produto'),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Rotas de Integração (APIs/Webhooks)
    path('pagamento/pix/<int:pedido_id>/', views.gerar_pix, name='gerar_pix'),
    path('webhooks/pix/', views.webhook_pix, name='webhook_pix'),
]
