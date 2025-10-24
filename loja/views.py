# loja/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Produto, Pedido
import json
import requests
import os

# --- MÓDULO PRINCIPAL (VIEWS DE VENDAS) ---

def home(request):
    """Página inicial com destaque de produtos."""
    # Note que a função 'home' está definida aqui.
    produtos_em_destaque = Produto.objects.filter(publicado=True)[:4]
    return render(request, 'loja/home.html', {'produtos': produtos_em_destaque})

def lista_produtos(request):
    """Lista todos os produtos disponíveis."""
    produtos = Produto.objects.filter(publicado=True)
    return render(request, 'loja/lista_produtos.html', {'produtos': produtos})

def detalhe_produto(request, produto_id):
    """Exibe detalhes de um produto e a opção de comprar."""
    produto = get_object_or_404(Produto, id=produto_id, publicado=True)
    return render(request, 'loja/detalhe_produto.html', {'produto': produto})

def adicionar_carrinho(request, produto_id):
    """Lógica para adicionar um produto ao carrinho (simulação)."""
    print(f"Produto {produto_id} adicionado ao carrinho (simulação).")
    return redirect('checkout')

def checkout(request):
    """Página de checkout para finalizar o pedido."""
    if request.method == 'POST':
        # Simula a criação do pedido no DB
        novo_pedido = Pedido.objects.create(status='PENDENTE', total=100.00) 
        return redirect('gerar_pix', pedido_id=novo_pedido.id)
    
    return render(request, 'loja/checkout.html', {'carrinho': 'Itens no Carrinho'})

# --- INTEGRAÇÃO PIX (Gera a Cobrança) ---

PIX_API_URL = os.environ.get("PIX_API_URL", "https://api.provedorpix.com/cobranca")

def gerar_pix(request, pedido_id):
    """Chama a API do provedor para gerar o QR Code PIX (Simulação)."""
    pedido = get_object_or_404(Pedido, id=pedido_id, status='PENDENTE')
    
    dados_cobranca = {
        "valor": str(pedido.total),
        "txid": f"PEDIDO{pedido.id}",
        "webhook_url": "http://seu-dominio.com/webhooks/pix/" 
    }
    
    try:
        # Simulação de resposta da API
        pix_data = {
            'qr_code_base64': 'BASE64_DO_QR_CODE', 
            'pix_copia_e_cola': '00020126...',
            'cobranca_id': 'ID_DO_PROVEDOR_123'
        }
        
        pedido.pix_cobranca_id = pix_data['cobranca_id']
        pedido.save()
        
        return render(request, 'loja/pagamento_pix.html', pix_data)
        
    except Exception as e:
        return HttpResponse(f"Erro ao gerar PIX: {e}", status=500)


# --- INTEGRAÇÃO PIX (RECEBE A CONFIRMAÇÃO) ---

@csrf_exempt 
@require_http_methods(["POST"])
def webhook_pix(request):
    """Recebe a notificação de pagamento (Webhook) do provedor de PIX (Simulação)."""
    try:
        data = json.loads(request.body)
        pix_id = data.get('id_cobranca') 
        status_pagamento = data.get('status')
        
        if status_pagamento == 'PAGO':
            pedido = Pedido.objects.get(pix_cobranca_id=pix_id, status='PENDENTE')
            pedido.status = 'PAGO'
            pedido.save()
            
        return HttpResponse("Webhook recebido e processado.", status=200)

    except (json.JSONDecodeError, Pedido.DoesNotExist):
        return HttpResponse("Erro ou pedido não encontrado.", status=400)
    except Exception as e:
        print(f"Erro no processamento do webhook: {e}")
        return HttpResponse("Erro interno.", status=500)
