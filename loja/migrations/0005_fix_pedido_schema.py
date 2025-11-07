from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("loja", "0004_create_logwhatsapps"),
    ]

    operations = [
        # Garante a coluna `nome` em Postgres (idempotente)
        migrations.RunSQL(
            sql="""
                ALTER TABLE loja_pedido
                ADD COLUMN IF NOT EXISTS nome varchar(255);
            """,
            reverse_sql="""
                -- Não remova a coluna no rollback
                DO $$ BEGIN END $$;
            """,
        ),
        # Garante tipos/auto_now dos timestamps (não destrutivo)
        migrations.RunSQL(
            sql="""
                ALTER TABLE loja_pedido
                ALTER COLUMN criado_em TYPE timestamp with time zone,
                ALTER COLUMN atualizado_em TYPE timestamp with time zone;
            """,
            reverse_sql="""
                DO $$ BEGIN END $$;
            """,
        ),
        # Para o ORM “saber” do campo `nome` (caso o histórico local tenha divergido)
        migrations.AlterField(
            model_name="pedido",
            name="nome",
            field=models.CharField(max_length=255, blank=False),
        ),
    ]
