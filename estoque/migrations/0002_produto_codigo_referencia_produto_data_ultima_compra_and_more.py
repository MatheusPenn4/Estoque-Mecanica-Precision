# Generated by Django 4.2.7 on 2025-05-30 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='codigo_referencia',
            field=models.CharField(default=2, max_length=50, unique=True, verbose_name='Código de Referência'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='data_ultima_compra',
            field=models.DateField(blank=True, null=True, verbose_name='Data da Última Compra'),
        ),
        migrations.AddField(
            model_name='produto',
            name='fornecedor',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Fornecedor'),
        ),
        migrations.AddField(
            model_name='produto',
            name='localizacao',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Localização na Prateleira'),
        ),
        migrations.AddField(
            model_name='produto',
            name='prazo_entrega',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Prazo de Entrega (dias)'),
        ),
    ]
