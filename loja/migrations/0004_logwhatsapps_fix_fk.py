# loja/migrations/0004_logwhatsapps_fix_fk.py
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0003_alter_timestamp_autos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logwhatsapps',
            name='pedido',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='logs',
                to='loja.pedido',
                null=True,
                blank=True,
            ),
        ),
    ]
