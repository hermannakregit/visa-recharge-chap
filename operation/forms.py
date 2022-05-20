from django.forms import ModelForm

from operation.models import Operation

class OperationForm(ModelForm):
    class Meta:
        model = Operation
        fields = ['montant_operation']

    def __init__(self, *args, **kwargs):
        super(OperationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control text-center'})