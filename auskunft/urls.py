from django.conf.urls import patterns, url

from auskunft.views import InformationRequestWizard
from auskunft.forms import AuftraggeberForm, AddressForm, AdditionalInfoForm

urlpatterns = patterns('',
    url(r'^$', InformationRequestWizard.as_view([AuftraggeberForm,AddressForm,AdditionalInfoForm])),
)
