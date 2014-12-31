from django.conf.urls import patterns, url

from auskunft.views import InformationRequestWizard
from auskunft.forms import AuftraggeberForm, AddressForm, AdditionalInfoForm, ProofOfIdentityForm

ir_wizard_forms = [AuftraggeberForm,AddressForm,AdditionalInfoForm,ProofOfIdentityForm]

urlpatterns = patterns('',
    url(r'^$', InformationRequestWizard.as_view(ir_wizard_forms)),
)
