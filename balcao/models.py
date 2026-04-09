from django.db import models


class UnidadeProduto(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_unidade = models.CharField(max_length=5)


    def __str__(self):
        return self.tipo_unidade


class Produtos(models.Model):

    id = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=100)
    tipo_produto = models.ForeignKey(UnidadeProduto, on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    estoque = models.FloatField(default=0, verbose_name="Estoque Atual")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Criação")    
    ultima_alteracao = models.DateTimeField(auto_now=True, verbose_name="Ultima Alteração")    


    def __str__(self):
        return self.nome_produto 
    

class VendasBalcao(models.Model):

    id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT)
    unidade = models.ForeignKey(UnidadeProduto, on_delete=models.PROTECT, null=True, blank=True) 
    preco = models.FloatField(blank=True, null=True)
    quantidade = models.FloatField(max_length=20)
    total = models.FloatField(blank=True, null=True)
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)


    def save(self, *args, **kwargs):
        if self.produto:

            self.unidade = self.produto.tipo_produto
            self.preco = self.produto.preco
            
            if self.quantidade and self.preco:
                valor_bruto = "{:.2f}".format(self.quantidade * self.preco)
                self.total = valor_bruto

        super().save(*args, **kwargs)


    def __str__(self):
        return self.produto.nome_produto


