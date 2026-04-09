from django.db.models import Max, Min
from django.db.models.functions import Trim, Lower
from django.shortcuts import render, redirect
from balcao.models import Produtos, VendasBalcao
from balcao.forms import ProdutoForm, VendaForm


def balcao_view(request):
    balcao = Produtos.objects.select_related("tipo_produto")
    search = request.GET.get("busca")

    if search:        
        balcao = balcao.filter(nome_produto__icontains=search)
    # usando metodo do querySet annotate para deixar o nome_produto sem espaços e minusculo para aplicar o order_by
    balcao = balcao.annotate(nome_limpo=Lower(Trim("nome_produto"))).order_by("nome_limpo") 
    quantidade_produtos = balcao.count()
    precos = balcao.aggregate(maior=Max("preco"), menor=Min("preco"))

    # ## Caso queira pegar o nome junto com o preco preciso pegar o objeto todo conforme abaixo
    # maior = balcao.order_by("-preco").first()
    # menor = balcao.order_by("-preco").last()
    # ## no HTML agora posso passar maior.preco e maior.nome_produto 

    return render(
    
        request,
        "balcao.html", 
        {"balcao": balcao,
         "quantidade_produtos": quantidade_produtos,
         "maior_preco": precos['maior'],
         "menor_preco": precos['menor'],
         }
    )


def novo_prod_view(request):

    if request.method == "POST":
        novo_prod_form = ProdutoForm(request.POST)

        if novo_prod_form.is_valid():
            novo_prod_form.save()
            return redirect("balcao_list")
    
    else:
        novo_prod_form = ProdutoForm()

    return render(
        request,
        "novo_produto.html",
        {"novo_prod_form": novo_prod_form}

    )

def venda_view(request):
    
    if request.method == "POST":
        nova_venda_form = VendaForm(request.POST, request.FILES)

        if nova_venda_form.is_valid():
            nova_venda_form.save()
            return redirect("balcao_list") 

    else:
        nova_venda_form = VendaForm()

    precos = Produtos.objects.values("id", "preco")    
    precos_dict = {item["id"]: float(item["preco"]) for item in precos}


    return render(
        request,
        "vendas.html",
        {"nova_venda_form": nova_venda_form,
         "precos_dict": precos_dict,
         })


def historico_view(request):
    
    vendas = VendasBalcao.objects.select_related("produto", "unidade").order_by("-id")
    
    total_faturamento = 0
    maior_venda = 0
    nome_produto = "Nenhum"
    # usando metodo exists() o django verifica de uma forma mais explicita se a QuerySet
    # tem valores dentro. Usamos 'exists()' em QuerySet.
    if vendas.exists():

        for venda in vendas:
            total_faturamento += venda.total

        total_faturamento = round(total_faturamento, 2)

        ## compreensao geradora para iterar sobre o atributo total do meu objeto.
        ## faz o mesmo que o for acima, de forma mais simplificada.
        # total_geral = round(sum(v.total for v in VendasBalcao.objects.all()), 2)

        # iniciando o objeto com o maior valor de venda.
        obj_maior_venda = vendas.order_by("-total").first()        
        # Verifica se o maior valor do 'obj_maior_venda' foi encontrado.
        if obj_maior_venda:
            
            maior_venda = obj_maior_venda.total
            nome_produto = obj_maior_venda.produto.nome_produto


    return render(
        request,
        "historico.html",
        
        {"vendas": vendas, 
         "total_faturamento": total_faturamento, 
         "maior_venda": maior_venda, 
         "nome_produto": nome_produto 
         }
    )


