from django import forms
from balcao.models import UnidadeProduto, Produtos, VendasBalcao


class ProdutoForm(forms.Form):

    nome_produto = forms.CharField(max_length=100)
    tipo_produto = forms.ModelChoiceField(UnidadeProduto.objects.all())
    preco = forms.FloatField()
    estoque = forms.FloatField()


    def save(self):

        prod = Produtos(
            nome_produto = self.cleaned_data["nome_produto"],
            tipo_produto = self.cleaned_data["tipo_produto"],
            preco = self.cleaned_data["preco"],
            estoque = self.cleaned_data["estoque"],
        )
        prod.save()
        return prod


class VendaForm(forms.Form):
    
    produto = forms.ModelChoiceField(Produtos.objects.all())
    quantidade = forms.DecimalField(max_digits=8, decimal_places=3)
    imagem = forms.ImageField()

    def save(self):
        
        venda = VendasBalcao(
            produto = self.cleaned_data["produto"],
            quantidade = self.cleaned_data["quantidade"],
            imagem = self.cleaned_data["imagem"]
        )

        venda.save()
        return venda
