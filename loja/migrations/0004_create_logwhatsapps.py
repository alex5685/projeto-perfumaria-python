# loja/migrations/0004_create_logwhatsapps.py
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("loja", "0003_alter_timestamp_autos"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogWhatsapps",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("telefone", models.CharField(blank=True, max_length=30)),
                ("mensagem", models.TextField(blank=True)),
                ("status", models.CharField(blank=True, max_length=50)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                (
                    "pedido",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="logs",
                        to="loja.pedido",
                        null=True,
                        blank=True,
                    ),
                ),
            ],
            options={
                "ordering": ["-criado_em"],
                "verbose_name": "Log de WhatsApp",
                "verbose_name_plural": "Logs de WhatsApp",
            },
        ),
    ]
