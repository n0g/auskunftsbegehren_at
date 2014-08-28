import datetime
from io import BytesIO

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext as _

from dinbrief.document import Document
from dinbrief.template import BriefTemplate
from dinbrief.styles import styles
from reportlab.platypus import Spacer, Paragraph, ListFlowable, ListItem
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.units import cm,mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

from auskunft.forms import AddressForm, additional_info_form_factory

from auskunft.models import Auftraggeber, Application


def address(request):
    form = AddressForm()
    return render(request,'auskunft/address.html',{'form':form})

def addinfo(request):
    form = AddressForm(request.POST)
    if not form.is_valid():
        raise Http404
    auftraggeber = form.cleaned_data['auftraggeber']
    AdditionalInfoForm = additional_info_form_factory(auftraggeber)
    new_form = AdditionalInfoForm()
    return render(request,'auskunft/addinfo.html',{'form':new_form})

def delivery(request):
    return HttpResponse("Nett.")

def create(request):
    form = AuskunftForm(request.POST)
    if form.is_valid():
        # get data from form
        auftraggeber = form.cleaned_data['auftraggeber']
        add_info = form.cleaned_data['additional_info']

        # prepare pdf data
        sender_address = create_sender_address(form)
        recipient_address = create_recipient_address(auftraggeber)
        content = create_content(form)

        date = datetime.datetime.now().strftime("%d.%m.%Y")

        # create document structure
        document = Document(
            sender=sender_address,
            recipient=recipient_address,
            date=date,
            content=content
        )

        # create pdf
        response = create_pdf_response(document)
        return response
    else:
        raise Http404

# TODO: refactor file and move pdf generation to separate file

def create_content(form):
    # TODO: move styles somewhere else
    # style for additional information box
    ibs = ParagraphStyle('inputBoxStyle',styles['Message'])
    ibs.fontName = 'Courier'
    ibs.leftIndent = cm
    ibs.spaceBefore = 0.2*cm
    ibs.spaceAfter = 0.5*cm
    # style for table of applications
    table_style = TableStyle([
            ('VALIGN',(0,0),(0,-1),'TOP')
        ])
    # font style for letter subject
    styles['Subject'].fontName = 'Helvetica-Bold'

    # TODO: move application list processing in seperate function
    # list of applications
    apps = Application.objects.filter(auftraggeber=form.cleaned_data['auftraggeber'],state__contains="Registriert")
    list_apps = [
        [Paragraph(x.number,styles['Message']),
        Paragraph(x.description,styles['Message'])] for x in apps]
    table_apps = Table(list_apps,colWidths=[3*cm,14*cm])
    table_apps.setStyle(table_style)

    content = [
        Paragraph(_("auskunft_subject"), styles['Subject']),
        Paragraph(_("auskunft_greeting"), styles['Greeting']),
        Spacer(0,0.5*cm),
        Paragraph(_("auskunft_question_text"), styles['Message']),
        ListFlowable([
            ListItem(Paragraph(_("auskunft_question_1"),styles['Message'])),
            ListItem(Paragraph(_("auskunft_question_2"),styles['Message'])),
            ListItem(Paragraph(_("auskunft_question_3"),styles['Message'])),
            ListItem(Paragraph(_("auskunft_question_4"),styles['Message'])),
            ],
            bulletType='bullet',
            start='square'
        ),
        Paragraph(_("auskunft_reference"), styles['Message']),
        Paragraph(_("auskunft_par_10"), styles['Message']),
        Paragraph(_("auskunft_par_4"), styles['Message']),
        Paragraph(_("auskunft_par_12"), styles['Message']),

        Paragraph(_("auskunft_standard_application"), styles['Message']),
        Paragraph(_("auskunft_registered_application_pre"),styles['Message']),
        table_apps,
        Paragraph(_("auskunft_registered_application_post"),styles['Message']),


        Paragraph(_("auskunft_additional_info_text"), styles['Message']),
        Paragraph(form.cleaned_data['additional_info'],ibs),

        Paragraph(_("auskunft_method_identity"),styles['Message']),
        Paragraph(_("auskunft_expected_response"),styles['Message']),

        Spacer(0,0.5*cm),
        Paragraph(_("auskunft_signature"),styles['Signature']),
        Paragraph(form.cleaned_data['name'],styles['Signature']),
    ]

    return content

def create_recipient_address(auftraggeber):
    recipient_address = [ auftraggeber.name ] + \
        auftraggeber.address.splitlines() + \
        [ "E-Mail: " + auftraggeber.email]
    return recipient_address

def create_sender_address(form):
    sender_address = [ form.cleaned_data['name'] ] + \
        form.cleaned_data['address'].splitlines() + \
        [ "E-Mail: " + form.cleaned_data['email'] ]

    return sender_address

def create_pdf_response(document):
    # Create Buffer
    buff = BytesIO()

    # Build template
    template = BriefTemplate(buff, document)
    template.build(document.content)

    # Create Response and close Buffer
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = \
        'attachment; filename="auskunftsbegehren.pdf"'

    pdf_response = buff.getvalue()
    buff.close()
    response.write(pdf_response)

    return response
