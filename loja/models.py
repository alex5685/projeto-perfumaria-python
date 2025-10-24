from django.db import models
from django.contrib.auth.models import User

# --- MÓDULO SECUNDÁRIO (ADM/Controle) ---

class Produto(models.Model):
    """Modelo para Perfumes, Maquiagem e Cuidados Pessoais."""
    nome = models.CharField(max_length=200, verbose_name="Nome do Produto")
    descricao = models.TextField(verbose_name="Descrição Detalhada")
    preco = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço de Venda")
    
    # Controle de Estoque (Usado pelo ADM)
    estoque = models.IntegerField(default=0, verbose_name="Quantidade em Estoque")
    
    # Imagem (Gatilho para WhatsApp)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    
    # Status de Publicação (Define se o produto está no site)
    publicado = models.BooleanField(default=False, verbose_name="Disponível no Site")
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome
        
# --- MÓDULO PRINCIPAL (Vendas/Pedidos) ---

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pagamento Pendente'),
        ('PAGO', 'Pagamento Confirmado'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGUE', 'Entregue'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    total = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Dados para Integração PIX/Pagamento
    pix_cobranca_id = models.CharField(max_length=255, blank=True, null=True, 
                                       verbose_name="ID da Cobrança PIX")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        
    def __str__(self):
        return f"Pedido #{self.id} - {self.status}"

# Modelo para o WhatsApp (Log de Notificações)
class LogWhatsapp(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    data_envio = models.DateTimeField(auto_now_add=True)
    sucesso = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Log WhatsApp Produto {self.produto.nome}"

