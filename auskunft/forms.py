from django import forms
from auskunft.models import Auftraggeber

class AuskunftForm(forms.Form):
    auftraggeber = forms.ModelChoiceField(queryset=Auftraggeber.objects.all())
    name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    additional_info = forms.CharField(widget=forms.Textarea)
