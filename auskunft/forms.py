from django import forms
from auskunft.models import Auftraggeber, Application

class AddressForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    auftraggeber = forms.ModelChoiceField(queryset=Auftraggeber.objects.all())

class AdditionalInfoForm(forms.Form):
    additional_info = forms.CharField(widget=forms.Textarea)
    relevant_apps = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Application.objects.none())
