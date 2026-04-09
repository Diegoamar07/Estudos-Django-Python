from django.contrib import admin
from fornecedores.models import GrupoFornecedor, Fornecedores, OrdemCompra


class GrupoFornecedorAdmin(admin.ModelAdmin):
    list_display = ["nome_do_grupo"]
    search_fields = ["nome_do_grupo"]


class FornecedoresAdmin(admin.ModelAdmin):
    list_display = ["nome_fornecedor", "cnpj", "telefone", "email", "grupo_fornecedor", "foto_grupo_fornecedor"]
    search_fields = ["nome_fornecedor", "cnpj"]
    list_filter = ["grupo_fornecedor"]

    list_per_page = 5

# Este decorator ja REGISTRA a tabela 'OrdemCompra' no banco de dados mais moderno
# que colocar la no final admin.site.register(class tabela, class admin)
@admin.register(OrdemCompra)
class OrdemCompraAdmin(admin.ModelAdmin):
    
    # 1. Colunas que aparecem na lista (Tabela)
    list_display = ["numero_oc", "fornecedores", "grupo_fornec", "produto", "unidade", "preco_produto", "quantidade", "total_oc", "status", "descricao", "data_oc"]

    # 2. Barra de Busca (Pesquisa por número, nome do fornecedor ou produto)
    # Use o __ para buscar em outras tabelas
    search_fields = ["numero_oc", "fornecedores__nome_fornecedor", "produto__nome_produto"]

    # 3. Filtros Laterais (Para filtrar as 1.000 OCs rapidinho)
    # Isso cria botões na direita: "Aberto", "Ontem", "Fornecedor X"
    list_filter = [
        "status", 
        "fornecedores", 
        "data_oc"
    ]

    # 4. Navegação por Linha do Tempo (No topo do Admin)
    # Você clica no Ano > Mês > Dia para achar a compra
    date_hierarchy = "data_oc"

    # paginação
    list_per_page = 30


admin.site.register(GrupoFornecedor, GrupoFornecedorAdmin)
admin.site.register(Fornecedores, FornecedoresAdmin)
