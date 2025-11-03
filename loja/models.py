# loja/models.py
from django.db import models

class Produto(models.Model):
    nome = models.CharField("Nome do Produto", max_length=120)
    descricao = models.TextField("Descrição Detalhada", blank=True)
    preco_venda = models.DecimalField("Preço de Venda", max_digits=10, decimal_places=2)
    quantidade_estoque = models.PositiveIntegerField("Quantidade em Estoque", default=0)
    disponivel_no_site = models.BooleanField("Disponível no Site", default=True)

    # >>> AQUI é o ponto crítico: use "produtos/" (plural)
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.pk}"


class LogWhatsapp(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    conteudo = models.TextField()

    def __str__(self):
        return f"Log {self.pk}"
