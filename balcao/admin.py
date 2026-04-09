from django.contrib import admin
from balcao.models import Produtos, VendasBalcao, UnidadeProduto


class UnidadeProdutoAdmin(admin.ModelAdmin):

    list_display = ("tipo_unidade",)
    search_fields = ("tipo_unidade",)

class VendasBalcaoAdmin(admin.ModelAdmin):

    list_display = ("produto", "unidade", "preco", "quantidade", "total")
    readonly_fields = ["total", "preco", "unidade"]
    fields = ["produto", "unidade", "preco", "quantidade", "total", "imagem"]
    search_fields = ("produto",)


class ProdutosAdmin(admin.ModelAdmin):

    list_display = ("nome_produto", "tipo_produto", "preco")
    search_fields = ("nome_produto",)


admin.site.register(Produtos, ProdutosAdmin)
admin.site.register(VendasBalcao, VendasBalcaoAdmin)
admin.site.register(UnidadeProduto, UnidadeProdutoAdmin)
