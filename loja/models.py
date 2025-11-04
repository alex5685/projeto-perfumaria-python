# loja/models.py  (VERSÃO TEMPORÁRIA – PARA GERAR A MIGRAÇÃO SEM PROMPTS)
from django.db import models
from django.utils import timezone


class Produto(models.Model):
    nome = models.CharField(max_length=120)
    descricao_detalhada = models.TextField(blank=True, null=True)

    # defaults explícitos PARA POPULAR REGISTROS EXISTENTES (sem prompt)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_estoque = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    disponivel_no_site = models.BooleanField(default=True)

    # <<< AQUI a mudança TEMPORÁRIA: default=timezone.now ao invés de auto_now_add >>>
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='pedidos')
    quantidade = models.PositiveIntegerField(default=1)

    # <<< AQUI a mudança TEMPORÁRIA: default=timezone.now >>>
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Pedido #{self.pk} - {self.produto.nome}"


class LogWhatsapps(models.Model):
    mensagem = models.TextField()
    enviado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Log do WhatsApp"
        verbose_name_plural = "Logs do WhatsApp"

    def __str__(self):
        return f"Log {self.pk} - {self.enviado_em:%d/%m/%Y %H:%M}"
