from django import forms
from auskunft.models import Auftraggeber, Application

class AddressForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    auftraggeber = forms.ModelChoiceField(queryset=Auftraggeber.objects.all())

def additional_info_form_factory(auftraggeber):
    properties = {
            'additional_info': forms.CharField(widget=forms.Textarea),
            'relevant_apps': forms.ModelChoiceField(
                widget=forms.CheckboxSelectMultiple,
                queryset=Application.objects.filter(auftraggeber=auftraggeber,state__contains="Registriert"))
        }

    return type('AdditionalInfoForm',(forms.Form,),properties)
