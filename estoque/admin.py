from django.contrib import admin
from .models import Categoria, Produto, Movimentacao


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo_referencia', 'categoria', 'preco_unitario', 
                  'quantidade_em_estoque', 'estoque_minimo', 'localizacao', 
                  'fornecedor', 'valor_total_em_estoque', 'estoque_baixo')
    list_filter = ('categoria', 'fornecedor', 'data_cadastro')
    search_fields = ('nome', 'descricao', 'codigo_referencia', 'localizacao')
    date_hierarchy = 'data_cadastro'
    list_editable = ('preco_unitario', 'quantidade_em_estoque', 'estoque_minimo')
    readonly_fields = ('data_cadastro',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'codigo_referencia', 'descricao', 'categoria', 'imagem')
        }),
        ('Estoque', {
            'fields': ('quantidade_em_estoque', 'estoque_minimo', 'localizacao')
        }),
        ('Informações Financeiras', {
            'fields': ('preco_unitario',)
        }),
        ('Informações do Fornecedor', {
            'fields': ('fornecedor', 'data_ultima_compra', 'prazo_entrega')
        }),
    )


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'tipo', 'quantidade', 'data', 'responsavel')
    list_filter = ('tipo', 'data', 'responsavel')
    search_fields = ('produto__nome', 'observacao')
    date_hierarchy = 'data'
    readonly_fields = ('data',)
    autocomplete_fields = ['produto']
