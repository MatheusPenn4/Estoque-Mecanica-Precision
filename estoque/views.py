from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Q, Count
from django.db.models.functions import Coalesce
from django.http import HttpResponse
import csv
from datetime import datetime

from .models import Produto, Categoria, Movimentacao
from .forms import ProdutoForm, CategoriaForm, EntradaEstoqueForm, SaidaEstoqueForm, RelatorioEstoqueForm


def inicio(request):
    """Página inicial do sistema - Dashboard"""
    produtos = Produto.objects.all().select_related('categoria')
    produtos_baixo_estoque = produtos.filter(quantidade_em_estoque__lte=F('estoque_minimo'))
    total_produtos = produtos.count()
    total_categorias = Categoria.objects.count()
    
    # Valor total em estoque
    valor_total = produtos.aggregate(
        total=Sum(F('preco_unitario') * F('quantidade_em_estoque'), output_field=DecimalField())
    )['total'] or 0
    
    # Estatísticas das categorias
    categorias = Categoria.objects.annotate(
        qtd_produtos=Count('produtos'),
        valor_total=Sum(F('produtos__preco_unitario') * F('produtos__quantidade_em_estoque'), output_field=DecimalField())
    ).order_by('-valor_total')
    
    # Produtos mais valiosos
    produtos_valiosos = produtos.annotate(
        valor_total=ExpressionWrapper(
            F('preco_unitario') * F('quantidade_em_estoque'), 
            output_field=DecimalField()
        )
    ).order_by('-valor_total')[:5]
    
    # Últimas movimentações
    ultimas_movimentacoes = Movimentacao.objects.select_related('produto', 'responsavel').all()[:10]
    
    context = {
        'produtos': produtos,
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'valor_total': valor_total,
        'categorias': categorias,
        'produtos_valiosos': produtos_valiosos,
        'ultimas_movimentacoes': ultimas_movimentacoes,
    }
    return render(request, 'estoque/inicio.html', context)


@login_required
def lista_produtos(request):
    """Exibe a lista de produtos"""
    produtos = Produto.objects.all().select_related('categoria')
    
    # Filtragem por categoria
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)
    
    # Filtragem por termo de busca
    busca = request.GET.get('busca')
    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) | 
            Q(codigo_referencia__icontains=busca) |
            Q(localizacao__icontains=busca) |
            Q(fornecedor__icontains=busca)
        )
    
    # Filtragem por estoque baixo
    estoque_baixo = request.GET.get('estoque_baixo')
    if estoque_baixo == 'sim':
        produtos = produtos.filter(quantidade_em_estoque__lte=F('estoque_minimo'))
    
    categorias = Categoria.objects.all()
    
    context = {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_id': int(categoria_id) if categoria_id else None,
        'busca': busca,
        'estoque_baixo': estoque_baixo,
    }
    return render(request, 'estoque/lista_produtos.html', context)


@login_required
def detalhe_produto(request, pk):
    """Exibe detalhes de um produto específico"""
    produto = get_object_or_404(Produto, pk=pk)
    movimentacoes = produto.movimentacoes.all()[:10]  # Últimas 10 movimentações
    
    context = {
        'produto': produto,
        'movimentacoes': movimentacoes,
    }
    return render(request, 'estoque/detalhe_produto.html', context)


@login_required
def criar_produto(request):
    """Formulário para criar novo produto"""
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto {produto.nome} criado com sucesso!')
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    
    context = {'form': form, 'titulo': 'Adicionar Produto'}
    return render(request, 'estoque/form_produto.html', context)


@login_required
def editar_produto(request, pk):
    """Formulário para editar um produto existente"""
    produto = get_object_or_404(Produto, pk=pk)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produto {produto.nome} atualizado com sucesso!')
            return redirect('detalhe_produto', pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)
    
    context = {'form': form, 'titulo': f'Editar Produto: {produto.nome}'}
    return render(request, 'estoque/form_produto.html', context)


@login_required
def excluir_produto(request, pk):
    """Exclui um produto"""
    produto = get_object_or_404(Produto, pk=pk)
    
    if request.method == 'POST':
        nome_produto = produto.nome
        produto.delete()
        messages.success(request, f'Produto {nome_produto} excluído com sucesso!')
        return redirect('lista_produtos')
    
    context = {'objeto': produto}
    return render(request, 'estoque/confirmar_exclusao.html', context)


@login_required
def lista_categorias(request):
    """Exibe a lista de categorias"""
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'estoque/lista_categorias.html', context)


@login_required
def criar_categoria(request):
    """Formulário para criar nova categoria"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria {categoria.nome} criada com sucesso!')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    
    context = {'form': form, 'titulo': 'Adicionar Categoria'}
    return render(request, 'estoque/form_categoria.html', context)


@login_required
def editar_categoria(request, pk):
    """Formulário para editar uma categoria existente"""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f'Categoria {categoria.nome} atualizada com sucesso!')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    context = {'form': form, 'titulo': f'Editar Categoria: {categoria.nome}'}
    return render(request, 'estoque/form_categoria.html', context)


@login_required
def excluir_categoria(request, pk):
    """Exclui uma categoria"""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        nome_categoria = categoria.nome
        try:
            categoria.delete()
            messages.success(request, f'Categoria {nome_categoria} excluída com sucesso!')
        except:
            messages.error(request, f'Não foi possível excluir a categoria {nome_categoria} pois ela possui produtos associados.')
        return redirect('lista_categorias')
    
    context = {'objeto': categoria}
    return render(request, 'estoque/confirmar_exclusao.html', context)


@login_required
def entrada_estoque(request):
    """Formulário para registrar entrada em estoque"""
    produto_id = request.GET.get('produto_id')
    initial_data = {}
    
    if produto_id:
        try:
            produto = Produto.objects.get(pk=produto_id)
            initial_data['produto'] = produto
        except Produto.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = EntradaEstoqueForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.tipo = 'entrada'
            movimentacao.responsavel = request.user
            movimentacao.save()
            messages.success(request, 'Entrada registrada com sucesso!')
            return redirect('lista_movimentacoes')
    else:
        form = EntradaEstoqueForm(initial=initial_data)
    
    context = {'form': form, 'titulo': 'Registrar Entrada em Estoque'}
    return render(request, 'estoque/form_movimentacao.html', context)


@login_required
def saida_estoque(request):
    """Formulário para registrar saída de estoque"""
    produto_id = request.GET.get('produto_id')
    initial_data = {}
    
    if produto_id:
        try:
            produto = Produto.objects.get(pk=produto_id)
            initial_data['produto'] = produto
        except Produto.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = SaidaEstoqueForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.tipo = 'saida'
            movimentacao.responsavel = request.user
            movimentacao.save()
            messages.success(request, 'Saída registrada com sucesso!')
            return redirect('lista_movimentacoes')
    else:
        form = SaidaEstoqueForm(initial=initial_data)
    
    context = {'form': form, 'titulo': 'Registrar Saída de Estoque'}
    return render(request, 'estoque/form_movimentacao.html', context)


@login_required
def lista_movimentacoes(request):
    """Exibe a lista de movimentações"""
    movimentacoes = Movimentacao.objects.all()
    
    # Filtragem opcional
    tipo = request.GET.get('tipo')
    if tipo:
        movimentacoes = movimentacoes.filter(tipo=tipo)
    
    produto_id = request.GET.get('produto')
    if produto_id:
        movimentacoes = movimentacoes.filter(produto_id=produto_id)
    
    context = {
        'movimentacoes': movimentacoes,
        'tipo': tipo,
        'produto_id': int(produto_id) if produto_id else None,
        'produtos': Produto.objects.all(),
    }
    return render(request, 'estoque/lista_movimentacoes.html', context)


@login_required
def relatorio_estoque(request):
    """Gera relatórios sobre o estoque"""
    produtos = None
    form = RelatorioEstoqueForm(request.GET or None)
    
    if form.is_valid():
        tipo_relatorio = form.cleaned_data['tipo_relatorio']
        
        if tipo_relatorio == 'todos':
            produtos = Produto.objects.all()
        
        elif tipo_relatorio == 'categoria':
            categoria = form.cleaned_data.get('categoria')
            if categoria:
                produtos = Produto.objects.filter(categoria=categoria)
        
        elif tipo_relatorio == 'estoque_baixo':
            produtos = Produto.objects.filter(quantidade_em_estoque__lte=F('estoque_minimo'))
    
    # Se for solicitada exportação em CSV
    if 'exportar_csv' in request.GET and produtos:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="relatorio_estoque_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Nome', 'Categoria', 'Preço Unitário', 'Quantidade em Estoque', 'Valor Total'])
        
        for produto in produtos:
            writer.writerow([
                produto.id,
                produto.nome,
                produto.categoria.nome,
                produto.preco_unitario,
                produto.quantidade_em_estoque,
                produto.valor_total_em_estoque()
            ])
        
        return response
    
    context = {
        'form': form,
        'produtos': produtos,
    }
    return render(request, 'estoque/relatorio_estoque.html', context)
