from django import forms
from fornecedores.models import GrupoFornecedor, Fornecedores, OrdemCompra


class NovoGrupo(forms.Form):
    nome_do_grupo = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome...'}))
    descricao = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'rows': 5, 'cols': 30, 
        'placeholder': 'Descreva o grupo...'}), required=False)

        ## poderia estilizar o campo diretamente aqui dentro do textarea
        ## 'style': 'font-size: 14px; font-family: Arial, sans-serif;',

    def save(self):

        grupo = GrupoFornecedor(
            nome_do_grupo = self.cleaned_data["nome_do_grupo"],
            descricao = self.cleaned_data["descricao"],            
        )
        grupo.save()
        return grupo


class NovoFornec(forms.Form):

    nome_fornecedor = forms.CharField(max_length=200)
    cnpj = forms.CharField(max_length=18)
    telefone = forms.CharField(max_length=20)
    email = forms.EmailField()
    grupo_fornecedor = forms.ModelChoiceField(GrupoFornecedor.objects.all())
    foto_grupo_fornecedor = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    descricao = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)


    def save(self, id_fornecedor=None):

        dados = self.cleaned_data

        if id_fornecedor:
            # 2. LÓGICA DE EDITAR: busca o cara que já existe
            fornecedor = Fornecedores.objects.get(id=id_fornecedor)
            fornecedor.nome_fornecedor = dados["nome_fornecedor"]
            fornecedor.cnpj = dados["cnpj"]
            fornecedor.telefone = dados["telefone"]
            fornecedor.email = dados["email"]
            fornecedor.grupo_fornecedor = dados["grupo_fornecedor"]
            # Só troca a foto se o usuário subiu uma nova
            if dados["foto_grupo_fornecedor"]:
                fornecedor.foto_grupo_fornecedor = dados["foto_grupo_fornecedor"]
            fornecedor.descricao = dados["descricao"]
    
            fornecedor.save() # Aqui ele faz o UPDATE
            return fornecedor
        
        else:
            novo_fornec = Fornecedores(
            nome_fornecedor = self.cleaned_data["nome_fornecedor"],
            cnpj = self.cleaned_data["cnpj"],
            telefone = self.cleaned_data["telefone"],
            email = self.cleaned_data["email"],
            grupo_fornecedor = self.cleaned_data["grupo_fornecedor"],
            foto_grupo_fornecedor = self.cleaned_data["foto_grupo_fornecedor"],
            descricao = self.cleaned_data["descricao"],
            )
            novo_fornec.save()
            return novo_fornec


class OrdemCompraForm(forms.ModelForm):
    class Meta:
        model = OrdemCompra
        # listar apenas os campos que o usuario digita.
        fields = ["fornecedores", "produto", "quantidade", "status", "descricao"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # LÓGICA DE EXIBIÇÃO DO STATUS:
        # Se self.instance.pk existe, significa que a OC já está no banco (EDIÇÃO)
        if self.instance.pk:
            # Na edição, permitimos que ele veja ABERTO ou mude para CANCELADO
            self.fields['status'].choices = [
                ("ABERTO", "ABERTO"),
                ("CANCELADO", "CANCELADO"),
            ]
        else:
            # Se não tem PK, é uma OC nova (GERAR)
            # Forçamos a única opção visível como ABERTO
            self.fields['status'].choices = [("ABERTO", "ABERTO")]

      
