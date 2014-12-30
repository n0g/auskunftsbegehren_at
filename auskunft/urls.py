from django.conf.urls import patterns, url

from auskunft.views import InformationRequestWizard
from auskunft.forms import AddressForm, AdditionalInfoForm

urlpatterns = patterns('',
    url(r'^$', InformationRequestWizard.as_view([AddressForm,AdditionalInfoForm])),
)
