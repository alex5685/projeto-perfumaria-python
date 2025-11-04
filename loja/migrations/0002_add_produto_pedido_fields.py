# loja/migrations/0002_add_produto_pedido_fields.py
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ("loja", "0001_initial"),
    ]

    operations = [
        # PRODUTO
        migrations.AddField(
            model_name="produto",
            name="descricao_detalhada",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="produto",
            name="preco_venda",
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AddField(
            model_name="produto",
            name="quantidade_estoque",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="produto",
            name="disponivel_no_site",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="produto",
            name="criado_em",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="produto",
            name="atualizado_em",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),

        # PEDIDO
        migrations.AddField(
            model_name="pedido",
            name="criado_em",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
