from django.forms import ModelForm

from carte.models import Carte

class CarteForm(ModelForm):
    class Meta:
        model = Carte
        fields = [
            'type_carte', 
            'carte_client_id', 
            'carte_num', 
            'carte_exp_month', 
            'carte_exp_year',
            ]

    def __init__(self, *args, **kwargs):
        super(CarteForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})