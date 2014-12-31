# -*- coding: utf-8 -*-

from django import forms
from auskunft.models import Auftraggeber, Application, IdentityProof

class AuftraggeberForm(forms.Form):
    auftraggeber = \
    forms.ModelChoiceField(queryset=Auftraggeber.objects.all(), \
    label='Auftraggeber')

class AddressForm(forms.Form):
    name = forms.CharField(max_length=100, label='Voller Name')
    address = forms.CharField(widget=forms.Textarea, label='Adresse')
    email = forms.EmailField(label='E-Mail Adresse')

class AdditionalInfoForm(forms.Form):
    relevant_apps = \
    forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, \
    queryset=Application.objects.none(), required=False, \
    label='Relevante Datenanwendungen in denen sich Daten ueber mich\
    befinden koennten (im Rahmen der Mitwirkungspflicht)')
    additional_info = \
    forms.CharField(widget=forms.Textarea,required=False, \
    label='Zusaetzliche Informationen (im Rahmen der Mitwirkungspflicht)')

class ProofOfIdentityForm(forms.Form):
    identity = forms.ModelChoiceField(queryset=IdentityProof.objects.all(), \
    widget=forms.Select, label='Form des \
    Identitaetsnachweises', required=False)
