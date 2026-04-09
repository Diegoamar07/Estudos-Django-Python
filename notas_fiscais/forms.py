from django import forms
from notas_fiscais.models import NotasEntrada


class NotasEntradaForm(forms.ModelForm):

    class Meta:
        model = NotasEntrada
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['readonly'] = True

        if 'data_ordem' in self.fields:     
            self.fields['data_ordem'].required = False
            self.fields['data_ordem'].disabled = True
