# loja/models.py
from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_detalhada = models.TextField(blank=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_estoque = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)
    disponivel_no_site = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    # se no seu código antigo tinha “cliente”, “telefone” etc, dá pra pôr aqui,
    # mas vamos começar do mínimo para o admin não quebrar.
    nome = models.CharField("Nome do cliente / referência", max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} - {self.nome}"


class LogWhatsapps(models.Model):
    # ⚠️ AQUI estava o problema no Render:
    # NUNCA usar default=timezone.now numa FK.
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="logs",
        null=True,
        blank=True,
    )
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Log de Whatsapp"
        verbose_name_plural = "Logs de Whatsapp"

    def __str__(self):
        if self.pedido_id:
            return f"Log {self.id} (pedido {self.pedido_id})"
        return f"Log {self.id}"

