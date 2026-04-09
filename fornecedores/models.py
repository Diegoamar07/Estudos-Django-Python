from django.db import models
from balcao.models import Produtos
from decimal import Decimal


class GrupoFornecedor(models.Model):
    nome_do_grupo = models.CharField(max_length=50, verbose_name="Grupo do fornecedor")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição do Grupo")


    def __str__(self):
        return self.nome_do_grupo


class Fornecedores(models.Model):
    nome_fornecedor = models.CharField(max_length=200, verbose_name="Razão social")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(unique=True, verbose_name="E-mail de contato")
    grupo_fornecedor = models.ForeignKey(GrupoFornecedor, on_delete=models.PROTECT, verbose_name="Grupo fornecedor")
    foto_grupo_fornecedor = models.ImageField(upload_to="fornecedores/", blank=True, null=True, verbose_name="Foto Grupo de fornecedor")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição fornecedor")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Criação")
    ultima_alteracao = models.DateTimeField(auto_now=True, verbose_name="Ultima Alteração")
    

    def __str__(self):
        return self.nome_fornecedor
    

class OrdemCompra(models.Model):

    # opções de escolha para o campo 'status' da tabela abaixo.
    STATUS_CHOICES = [
        ("ABERTO", 'ABERTO'),
        ("FECHADO", 'FECHADO'),
        ("CANCELADO", 'CANCELADO'),
    ]

    numero_oc = models.PositiveIntegerField(unique=True, editable=False, verbose_name="Número Ordem de Compra") 
    fornecedores = models.ForeignKey(Fornecedores, on_delete=models.PROTECT, verbose_name="Fornecedor")
    grupo_fornec = models.CharField(max_length=20, null=True, blank=True, editable=False, verbose_name="Grupo do Fornecedor")
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT, verbose_name="Nome Produto")
    unidade = models.CharField(max_length=10, null=True, blank=True, editable=False)
    preco_produto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False, verbose_name="Preço produto")
    quantidade = models.FloatField(verbose_name="Quantidade")
    total_oc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False, verbose_name="Total da OC.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ABERTO", verbose_name="Status da OC.")
    descricao = models.TextField(null=True, blank=True, verbose_name="Descriçao")
    data_oc = models.DateTimeField(auto_now_add=True, verbose_name="Data da Ordem de Compra")


    def __str__(self):
        return str(self.numero_oc)
        # return f"{self.numero_oc}, {self.fornecedores.nome_fornecedor}, {self.produto.nome_produto}"  

    
    def save(self, *args, **kwargs):
        # 1. Trava de segurança para impedir edição em OCs CONGELADAS
        if self.pk:
            oc_no_banco = OrdemCompra.objects.get(pk=self.pk)
            if oc_no_banco.status in ["CANCELADO", "FECHADO"]:
                raise ValueError("Esta Ordem de Compra está CONGELADA e não pode ser alterada.")

        # Garante que se NAO tiver uma OC vamos criar uma nova OC para salvar no banco.
        if not self.numero_oc:
            # capturando a ultima ordem de compra.
            ultimo = OrdemCompra.objects.all().order_by("numero_oc").last()
            
            if ultimo:
                # se ultimo for vazio(somente primeira vez que banco for vazio) o self.numero_oc vai entrar no else e vai ser 1.
                # proximas vezes o ultimo(objeto vai ter dados) entao(ultimo que e o objeto) e vamos
                # pegar o campo ultimo.numero_oc(campo que tem numero 1) e vamos somar + 1 para salvar
                # no self.numero_oc.
                self.numero_oc = ultimo.numero_oc + 1
            else:
                # se o banco estiver vazio. Começa com o numero 1.
                self.numero_oc = 1

        # Busca dados automaticos (sempre que salvar)
        if self.fornecedores:
            self.grupo_fornec = self.fornecedores.grupo_fornecedor.nome_do_grupo
        
        if self.produto:
            self.unidade = self.produto.tipo_produto.tipo_unidade
            self.preco_produto = self.produto.preco

        if self.preco_produto and self.quantidade:
            # a quantidade é float, preciso transformar em str e depois para Decimal para
            # equivaler ao campo preco_produto que e um decimal e entao fazer o calculo.
            self.total_oc = self.preco_produto * Decimal(str(self.quantidade))

        super().save(*args, **kwargs)

