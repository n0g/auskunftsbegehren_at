from django.contrib.formtools.wizard.views import CookieWizardView

from auskunft.models import Auftraggeber, Application
from auskunft.informationrequest import InformationRequest

class InformationRequestWizard(CookieWizardView):
    template_name = "auskunft/wizard.html"

    def get_form(self, step=None, data=None, files=None):
        form = super(InformationRequestWizard, self).get_form(step, data, files)
        # determine the step if not given
        if step is None:
            step = self.steps.current

        # set queryset for applications
        if step == '2':
            auftragg = self.get_cleaned_data_for_step('0')['auftraggeber']
            apps = Application.objects.filter(auftraggeber=auftragg,state__contains="Registriert").distinct()
            form.fields['relevant_apps'].queryset = apps

        return form

    def done(self, form_list, **kwargs):
        # parse content of form list
        data = self.get_all_cleaned_data()
        # call create method
        ir = InformationRequest()
        ir.set_sender(data['name'],data['address'],data['email'])
        ir.set_auftraggeber(data['auftraggeber'])
        if data['relevant_apps']:
            ir.set_relevant_apps(data['relevant_apps'])
        if data['additional_info']:
            ir.set_add_info(data['additional_info'])
        # return result page
        return ir.pdf_response()
