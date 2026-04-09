from django.db import models
from decimal import Decimal
from fornecedores.models import Fornecedores, OrdemCompra
from balcao.models import Produtos


class NotasEntrada(models.Model):

    numero_oc = models.ForeignKey(OrdemCompra, on_delete=models.PROTECT, verbose_name="Número OC")
    data_ordem = models.DateTimeField(null=True, blank=True, verbose_name="Data da OC")    
    fornecedor = models.ForeignKey(Fornecedores, on_delete=models.PROTECT, verbose_name="Nome do Fornecedor")
    grupo_fornec = models.CharField(max_length=20, null=True, blank=True, verbose_name="Grupo do Fornecedor")
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT, verbose_name="Produto")
    unidade = models.CharField(max_length=20, null=True, blank=True, verbose_name="Unidade")
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Preço unitário")
    quantidade = models.FloatField(null=True, blank=True, verbose_name="Quantidade")
    total_nota = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Total Nota Fiscal")
    status = models.CharField(max_length=20, choices=[('FECHADO', 'Fechado')], verbose_name="Status")
    descricao = models.TextField(null=True, blank=True, verbose_name="Descriçao")
    data_entrada = models.DateTimeField(auto_now_add=True, verbose_name="Data Entrada")
    numero_nota_entrada = models.IntegerField(verbose_name="Numero nota fiscal")


    def __str__(self):
        return f"{self.numero_oc.numero_oc}, {self.fornecedor.nome_fornecedor}, {self.produto.nome_produto}"


    def save(self, *args, **kwargs):

        if self.numero_oc:
            
            self.data_ordem = self.numero_oc.data_oc
            self.fornecedor = self.numero_oc.fornecedores
            self.grupo_fornec = self.numero_oc.grupo_fornec
            self.produto = self.numero_oc.produto
            self.unidade = self.numero_oc.unidade

            self.preco_unitario = self.numero_oc.preco_produto
            self.quantidade = self.numero_oc.quantidade

            if self.preco_unitario and self.quantidade:
                self.total_nota = self.preco_unitario * Decimal(str(self.quantidade)) 

        super().save(*args, **kwargs)




