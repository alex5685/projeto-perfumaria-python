# loja/migrations/0003_alter_timestamp_autos.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("loja", "0002_add_produto_pedido_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produto",
            name="criado_em",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="produto",
            name="atualizado_em",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="criado_em",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
