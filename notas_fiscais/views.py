from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from fornecedores.models import OrdemCompra
from notas_fiscais.forms import NotasEntradaForm


def notas_entrada_view(request):

    if request.method == "POST":
        notas_entrada = NotasEntradaForm(request.POST)
        
        if notas_entrada.is_valid():
            notas_entrada.save()
            return redirect("notas_entrada")

    else:
        notas_entrada = NotasEntradaForm()

    # .values retorna lista de DICIONARIO.
    ordens_obj = OrdemCompra.objects.values("id", "numero_oc", "fornecedores__id", "fornecedores__nome_fornecedor", "grupo_fornec", "produto__id", "produto__nome_produto", "unidade", "preco_produto", "quantidade", "total_oc", "status", "descricao", "data_oc")

    ordens_dict = { item["id"]:{"numero_oc":item['numero_oc'],
                                "fornecedor_id": item['fornecedores__id'],
                                "fornecedor": item['fornecedores__nome_fornecedor'],
                                "grupo_fornec": item['grupo_fornec'],
                                "produto_id": item['produto__id'],
                                "produto": item["produto__nome_produto"],
                                "unidade": item["unidade"],
                                "preco_produto": float(item["preco_produto"]),
                                "quantidade": float(item["quantidade"]),
                                "total_oc": float(item["total_oc"]),
                                "status": item["status"],
                                "descricao": item["descricao"],
                                "data_oc": item["data_oc"].strftime('%d-%m-%Y - Hrs: %H:%M') if item["data_oc"] else ""
                                } 
                                for item in ordens_obj }
 

    return render(
        request,
        "notas_entrada.html",
        {"notas_entrada": notas_entrada,
         "ordens_dict": ordens_dict}

    )


def notas_saida_view(request):
    pass


def get_oc_details(request, id_oc):
    # 1. Usa get_object_or_404 para não dar erro 500 se o ID for inválido
    oc = get_object_or_404(OrdemCompra, id=id_oc)

    dt_local = timezone.localtime(oc.data_oc) if oc.data_oc else None

    # 2. Monta o dicionário com verificações de segurança (if/else)
    data = {
        # Verifica se existe data para não dar erro no strftime
        "data_ordem": dt_local.strftime("%d-%m-%Y") if oc.data_oc else "",
        
        # Verifica se existe o objeto relacionado (ForeignKey)
        "fornecedor": oc.fornecedores.id if oc.fornecedores else "",
        
        # Ajustado para "grupo_fornec" com underline (como está no seu JS)
        "grupo_fornec": oc.grupo_fornec,
        
        "produto": oc.produto.id if oc.produto else "",
        "unidade": oc.unidade,
        "preco_unitario": str(oc.preco_produto),
        "quantidade": oc.quantidade,
        "status": oc.status,
        "total_oc": str(oc.total_oc) if oc.total_oc else "0.00",
    }

    return JsonResponse(data)
