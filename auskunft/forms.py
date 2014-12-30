from django import forms
from auskunft.models import Auftraggeber, Application

class AuftraggeberForm(forms.Form):
    auftraggeber = forms.ModelChoiceField(queryset=Auftraggeber.objects.all())

class AddressForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()

class AdditionalInfoForm(forms.Form):
    additional_info = forms.CharField(widget=forms.Textarea,required=False)
    relevant_apps = forms.ModelMultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple,queryset=Application.objects.none())
