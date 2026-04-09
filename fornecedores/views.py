from django.shortcuts import render, redirect, get_object_or_404
from fornecedores.models import Fornecedores, OrdemCompra
from fornecedores.forms import NovoFornec, NovoGrupo, OrdemCompraForm
from balcao.models import Produtos

# importando class Q para efetuar multiplos filtros no filter( Q(campo__icontains=busca) | Q....  )
from django.db.models import Q
# importanto class Paginator para criar paginas no navegador. Ele permite criar
# ex: 5 objetos por pagina. se tiver 15 OC's ele vai dividir 5 objetos por pagina.
from django.core.paginator import Paginator


def fornecedores_view(request):
    
    fornec = Fornecedores.objects.select_related("grupo_fornecedor")
    buscar = request.GET.get("busca")
    
    if buscar:
        fornec = fornec.filter(nome_fornecedor__icontains=buscar)

    fornec = fornec.order_by("nome_fornecedor")

    return render(
        request,
        "fornecedores.html",
        {"fornec": fornec},
    )


def novo_grupo_view(request):
    
    if request.method == "POST":
        novo_grupo_form = NovoGrupo(request.POST)

        if novo_grupo_form.is_valid():
            novo_grupo_form.save()
            return redirect("balcao_list")

    else:
        novo_grupo_form = NovoGrupo()

    return render(
        request,
        "novo_grupo.html",
        {"novo_grupo_form": novo_grupo_form},
    )


def novo_fornec_view(request):
    
    # 1. O Django lê o número que veio na URL após o '?id='
    id_fornecedor = request.GET.get("id")
    # 2. Criamos uma variável que começa vazia
    fornecedor_selecionado = None
    # 3. Se existir um ID, buscamos os dados desse fornecedor no Banco
    if id_fornecedor:
        fornecedor_selecionado = get_object_or_404(Fornecedores, id=id_fornecedor)

    if request.method == "POST":
        novo_fornec_form = NovoFornec(request.POST, request.FILES)

        if novo_fornec_form.is_valid():
            novo_fornec_form.save(id_fornecedor)
            return redirect("rel_comp_fornec")

    else:
        # Pega os dados do fornecedor se ele existir, senão fica None
        dados = fornecedor_selecionado.__dict__ if fornecedor_selecionado else None
        if dados:
            dados["grupo_fornecedor"] = fornecedor_selecionado.grupo_fornecedor

            # Verifica se existe foto e passa apenas o TEXTO do caminho
            if fornecedor_selecionado.foto_grupo_fornecedor:
                dados["foto_grupo_fornecedor"] = fornecedor_selecionado.foto_grupo_fornecedor.name

        novo_fornec_form = NovoFornec(initial=dados)

    return render(
        request,
        "novo_fornecedor.html",
        {"novo_fornec_form": novo_fornec_form,
         "fornecedor_selecionado": fornecedor_selecionado},
    )


def ordem_compra_view(request):

    id_oc = request.GET.get("id")
    instancia = get_object_or_404(OrdemCompra, id=id_oc) if id_oc else None

    if request.method == "POST":
        ordem_compra = OrdemCompraForm(request.POST, instance=instancia)

        if ordem_compra.is_valid():
            ordem_compra.save()
            return redirect("listar_ordens_compra")

    else:
        ordem_compra = OrdemCompraForm(instance=instancia)

    # iniciando queryset dict atraves do .values() para pegar somente o campo 'id' e 'preco' 
    precos = Produtos.objects.values("id", "preco", "tipo_produto__tipo_unidade")

    # Fazendo compreensao dict para fazer com que a chave "id" tenha seu valor ex: 1
    # e "preco" seja ex: 10. ficando precos_dict = {1: 10, 2: 12.20, etc...} 
    precos_dict = {item["id"]: [float(item["preco"]), item["tipo_produto__tipo_unidade"]] for item in precos} 


    return render(
        request,
        "ordem_compra.html",
        {"ordem_compra": ordem_compra,
         # passando nossa lista de precos em formato dict para o js filtrar agora.
         "precos_dict": precos_dict},
    )


def listar_ordem_compra(request):
    
    ordens_compra = OrdemCompra.objects.select_related("fornecedores", "produto")
    buscar = request.GET.get("busca")

    if buscar:    
        ordens_compra = ordens_compra.filter(
            Q(numero_oc__icontains=buscar) |
            Q(fornecedores__nome_fornecedor__icontains=buscar) |
            Q(produto__nome_produto__icontains=buscar)
        )

    ordens_compra = ordens_compra.order_by("-data_oc")

    # --- LÓGICA DE PAGINAÇÃO --- ***Importante: depois configurar o HTML.

    # 1 --> Paginator: O arquiteto (planeja as divisões).
    # 2 --> page_number: O mensageiro (traz a escolha do usuário da URL).
    # 3 --> page_obj: O entregador (leva os dados e os botões de navegação para o HTML).

    # instancia o objeto ex: se tiver 15 OC's o paginator cria 3 pacotes onde ele sabe
    # que pacote 1 tem 1 ao 5 objetos, o pacote 2 tem do 6 ao 10, etc..
    paginator = Paginator(ordens_compra, 5)
    # quando o usuario clica no link 2 da segunda pagina la no navegador o URl vai pegar
    # este numero 2 e guarda no page_number.
    page_number = request.GET.get("page")    
    # instancia o pacote com os 5 objetos para o HTML
    page_obj = paginator.get_page(page_number)


    return render(
        request,
        "lista_ordem_compra.html",
        {"ordens_compra": page_obj},
    )    


def rel_simples_fornec(request):

    rel_fornec_view = Fornecedores.objects.none()
    buscar = request.GET.get("busca")

    if buscar:
        rel_fornec_view = Fornecedores.objects.filter(nome_fornecedor__icontains=buscar).order_by("nome_fornecedor").values("nome_fornecedor", "email")


    return render(
        request,
        "rel_simples_fornec.html",
        {"rel_fornec_view": rel_fornec_view,
         "termo_buscado": buscar,
         }
    )


def rel_comp_fornec(request):
    
    buscar = request.GET.get("busca")
    fornecedores = Fornecedores.objects.none()

    if buscar:
        fornecedores = Fornecedores.objects.filter(nome_fornecedor__icontains=buscar).order_by("nome_fornecedor")

    return render(
        request,
        "rel_comp_fornec.html",
        {"fornecedores": fornecedores,
         "termo_buscado": buscar
         },
    )


