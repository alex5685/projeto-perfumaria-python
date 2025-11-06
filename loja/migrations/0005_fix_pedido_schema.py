from django.db import migrations

SQL = """
-- 1) Garante a coluna nome
ALTER TABLE loja_pedido ADD COLUMN IF NOT EXISTS nome varchar(255);

-- 2) Preenche valores nulos (se houver) e aplica NOT NULL
UPDATE loja_pedido SET nome = '' WHERE nome IS NULL;
ALTER TABLE loja_pedido ALTER COLUMN nome SET NOT NULL;

-- 3) (Defensivo) Garante timestamps caso o banco tenha sido criado sem eles
ALTER TABLE loja_pedido ADD COLUMN IF NOT EXISTS criado_em timestamptz DEFAULT now();
ALTER TABLE loja_pedido ADD COLUMN IF NOT EXISTS atualizado_em timestamptz DEFAULT now();

-- 4) Garante NOT NULL nos timestamps (opcional, mas alinhado ao modelo)
ALTER TABLE loja_pedido ALTER COLUMN criado_em SET NOT NULL;
ALTER TABLE loja_pedido ALTER COLUMN atualizado_em SET NOT NULL;
"""

class Migration(migrations.Migration):
    dependencies = [
        ("loja", "0004_create_logwhatsapps"),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL,
            reverse_sql=migrations.RunSQL.noop,  # não desfaz (seguro para produção)
        )
    ]
