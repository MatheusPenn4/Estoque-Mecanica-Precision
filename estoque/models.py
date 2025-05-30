from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Categoria(models.Model):
    nome = models.CharField("Nome", max_length=100, unique=True)
    descricao = models.TextField("Descrição", blank=True, null=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField("Nome", max_length=200)
    codigo_referencia = models.CharField(max_length=50, unique=True, verbose_name='Código de Referência')
    descricao = models.TextField("Descrição", blank=True, null=True)
    preco_unitario = models.DecimalField("Preço Unitário", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantidade_em_estoque = models.PositiveIntegerField("Quantidade em Estoque", default=0)
    estoque_minimo = models.PositiveIntegerField("Estoque Mínimo", default=5)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos', verbose_name="Categoria")
    localizacao = models.CharField(max_length=100, blank=True, null=True, verbose_name='Localização na Prateleira')
    fornecedor = models.CharField(max_length=200, blank=True, null=True, verbose_name='Fornecedor')
    data_ultima_compra = models.DateField(blank=True, null=True, verbose_name='Data da Última Compra')
    prazo_entrega = models.PositiveIntegerField(blank=True, null=True, verbose_name='Prazo de Entrega (dias)')
    imagem = models.ImageField("Imagem do Produto", upload_to='produtos/', blank=True, null=True)
    data_cadastro = models.DateTimeField("Data de Cadastro", default=timezone.now)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
        
    def valor_total_em_estoque(self):
        """Calcula o valor total deste produto em estoque"""
        # Convertendo explicitamente para garantir consistência de tipos
        return Decimal(self.preco_unitario) * Decimal(self.quantidade_em_estoque)
        
    def estoque_baixo(self):
        """Verifica se o produto está com estoque abaixo do mínimo"""
        return self.quantidade_em_estoque <= self.estoque_minimo


class Movimentacao(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='movimentacoes', verbose_name="Produto")
    tipo = models.CharField("Tipo", max_length=10, choices=TIPO_CHOICES)
    quantidade = models.PositiveIntegerField("Quantidade")
    data = models.DateTimeField("Data/Hora", default=timezone.now)
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Responsável")
    observacao = models.TextField("Observação", blank=True, null=True)
    
    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'
        ordering = ['-data']
    
    def __str__(self):
        return f"{self.get_tipo_display()} de {self.quantidade} {self.produto.nome} em {self.data.strftime('%d/%m/%Y %H:%M')}"
    
    def save(self, *args, **kwargs):
        """Sobrescrevendo o save para atualizar o estoque do produto"""
        # Se é uma nova movimentação (não tem ID ainda)
        if not self.pk:
            if self.tipo == 'entrada':
                self.produto.quantidade_em_estoque += self.quantidade
            else:  # saída
                if self.produto.quantidade_em_estoque >= self.quantidade:
                    self.produto.quantidade_em_estoque -= self.quantidade
                else:
                    raise ValueError("Quantidade insuficiente em estoque")
            
            self.produto.save()
        
        super().save(*args, **kwargs)
