from django.db import models


class Produto(models.Model):
    nome = models.CharField("Nome do Produto", max_length=255)
    descricao_detalhada = models.TextField("Descrição Detalhada", blank=True)
    preco_venda = models.DecimalField("Preço de Venda", max_digits=10, decimal_places=2)
    quantidade_estoque = models.PositiveIntegerField("Quantidade em Estoque", default=0)
    imagem = models.ImageField("Imagem", upload_to="produtos/", blank=True, null=True)
    disponivel_no_site = models.BooleanField("Disponível no Site", default=True)

    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ("-criado_em",)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    # Campos mínimos para o admin não quebrar.
    # (ajuste depois conforme sua regra de negócio)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ("-criado_em",)

    def __str__(self):
        return f"Pedido #{self.pk}"


class LogWhatsapps(models.Model):
    # Log simples (ajuste conforme sua necessidade)
    mensagem = models.TextField("Mensagem", blank=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Log whatsapp"
        verbose_name_plural = "Logs whatsapps"
        ordering = ("-criado_em",)

    def __str__(self):
        return f"Log #{self.pk}"
