from django.contrib import admin
from django.db.models import Q
from notas_fiscais.models import NotasEntrada
from fornecedores.models import OrdemCompra


@admin.register(NotasEntrada)
class NotasEntradaAdmin(admin.ModelAdmin):

    fields = ["numero_oc", "data_ordem", "fornecedor", "grupo_fornec",
              "produto", "unidade", "preco_unitario", "quantidade",
              "total_nota", "status", "descricao", "data_entrada", "numero_nota_entrada"]

    readonly_fields = ["data_ordem", "data_entrada"]

    search_fields = ["numero_oc__numero_oc", "fornecedor__nome_fornecedor"]

    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "numero_oc":
            # Pega as OCs de notas já fechadas
            fechadas = NotasEntrada.objects.filter(status='FECHADO').values_list('numero_oc_id', flat=True)
            
            # LÓGICA: Se NÃO for uma edição (estiver criando), aplica o filtro
            # O 'obj_id' na URL indica se estamos editando algo existente
            object_id = request.resolver_match.kwargs.get('object_id')
            
            if not object_id:
                # Na criação: Esconde as OCs já usadas
                kwargs["queryset"] = OrdemCompra.objects.exclude(id__in=fechadas)
            else:
                # Na edição: Permite que a OC da nota atual apareça no dropdown
                nota_atual = self.get_object(request, object_id)
                kwargs["queryset"] = OrdemCompra.objects.filter(
                    Q(id__in=OrdemCompra.objects.exclude(id__in=fechadas)) | 
                    Q(id=nota_atual.numero_oc_id)
                )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # LÓGICA PARA DESABILITAR OS CAMPOS NA EDIÇÃO
    def get_readonly_fields(self, request, obj=None):
        if obj: # Se o objeto já existe (está editando)
            # Retorna todos os campos como "apenas leitura"
            return [f.name for f in self.model._meta.fields] + ["data_entrada"]
        return self.readonly_fields


    # precisa ser este nome Media para o django reconhecer a classe que vai 
    # mostrar o caminho do arquivo .js para ler a tela no ADMIN somente.
    class Media():
        js = ["notas_entrada.js"]


