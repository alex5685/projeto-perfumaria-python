# loja/signals.py

from django.db.models.signals import post_save
# ... (restante dos imports)

# SUBSTITUA COM SUAS CREDENCIAIS REAIS DO WHAPI.CLOUD
WHATSAPP_API_URL = "https://gate.whapi.cloud/messages/image" # Adicionando /messages/image para a API de envio
WHATSAPP_API_TOKEN = "8AGQOpq4A2eQhiLJvJD1cZNABCGAZcNAY"
WHATSAPP_DESTINO = "5521972147510" # Seu número, no formato internacional: 55 + código de área + número

@receiver(post_save, sender=Produto)
def repostar_novo_produto_whatsapp(sender, instance, created, **kwargs):
    """Dispara a notificação de um novo produto publicado para o WhatsApp."""
    if created and instance.publicado:

        # ATENÇÃO: A URL da imagem DEVE ser acessível publicamente (no seu servidor)
        imagem_url_completa = f"http://seu-dominio.com{instance.imagem.url}"

        # Dados para a API do Whapi.Cloud
        dados_api = {
            "to": WHATSAPP_DESTINO,
            "token": WHATSAPP_API_TOKEN,
            # O Whapi.Cloud usa 'media' para a URL da imagem e 'caption' para a legenda
            "media": imagem_url_completa, 
            "caption": (
                f"🚨 NOVIDADE! Chegou o {instance.nome}!\n"
                f"💰 Preço: R$ {instance.preco:,.2f}\n"
                f"Clique aqui para ver: http://seu-dominio.com/produtos/{instance.id}"
            )
        }

        sucesso = False
        try:
            # Modificação: O Whapi.Cloud geralmente requer a URL da API específica para imagens.
            # Se for só gate.whapi.cloud/messages/send, pode funcionar, mas usei o /image por segurança.
            response = requests.post(WHATSAPP_API_URL, json=dados_api)
            response.raise_for_status() 
            sucesso = True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar para WhatsApp: {e}")

        LogWhatsapp.objects.create(produto=instance, sucesso=sucesso)
