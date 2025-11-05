from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_detalhada = models.TextField(blank=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_estoque = models.IntegerField(default=0)
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
    nome = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.pk}"


class LogWhatsapps(models.Model):
    """
    Log de eventos/integrações do WhatsApp.
    O vínculo com Pedido é opcional para não bloquear migração nem inserções.
    """

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="logs",
        null=True,
        blank=True,
    )
    telefone = models.CharField(max_length=30, blank=True)
    mensagem = models.TextField(blank=True)
    status = models.CharField(max_length=50, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Log de WhatsApp"
        verbose_name_plural = "Logs de WhatsApp"

    def __str__(self):
        return f"LogWhatsApp #{self.pk}"
