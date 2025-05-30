from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Produto, Categoria, Movimentacao


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome', 'codigo_referencia', 'descricao', 'preco_unitario', 
            'quantidade_em_estoque', 'estoque_minimo', 'categoria', 
            'localizacao', 'fornecedor', 'data_ultima_compra', 
            'prazo_entrega', 'imagem'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'data_ultima_compra': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar', css_class='btn btn-success'))


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar', css_class='btn btn-success'))


class EntradaEstoqueForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['produto', 'quantidade', 'observacao']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.tipo = 'entrada'
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar Entrada', css_class='btn btn-success'))


class SaidaEstoqueForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['produto', 'quantidade', 'observacao']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.tipo = 'saida'
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar Saída', css_class='btn btn-danger'))
    
    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        produto = self.cleaned_data.get('produto')
        
        if produto and quantidade > produto.quantidade_em_estoque:
            raise forms.ValidationError(
                f"Quantidade insuficiente em estoque. Disponível: {produto.quantidade_em_estoque}"
            )
        
        return quantidade


class RelatorioEstoqueForm(forms.Form):
    TIPO_RELATORIO_CHOICES = [
        ('todos', 'Todos os Produtos'),
        ('categoria', 'Produtos por Categoria'),
        ('estoque_baixo', 'Produtos com Estoque Baixo'),
    ]
    
    tipo_relatorio = forms.ChoiceField(choices=TIPO_RELATORIO_CHOICES, label="Tipo de Relatório")
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        label="Categoria"
    )
    
    limite_estoque = forms.IntegerField(
        label="Limite Mínimo de Estoque",
        required=False,
        min_value=0,
        initial=10
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('tipo_relatorio', css_class='form-group col-md-4'),
                Column('categoria', css_class='form-group col-md-4'),
                Column('limite_estoque', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Submit('submit', 'Gerar Relatório', css_class='btn btn-primary')
        )
