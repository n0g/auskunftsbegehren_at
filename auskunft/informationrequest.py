#! /usr/bin/env python
import datetime
from io import BytesIO

from django.http import HttpResponse
from django.utils.translation import ugettext as _

from dinbrief.document import Document
from dinbrief.template import BriefTemplate
from dinbrief.styles import styles
from reportlab.platypus import Spacer, Paragraph, ListFlowable, ListItem
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.units import cm,mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

from auskunft.models import Auftraggeber, Application

class InformationRequest():
    def __init__(self):
        self.sender_name = ""
        self.sender_address = [ "" ]
        self.recipient_address = [ "" ]
        self.add_info = ""
        self.table_apps = Table([[""]],colWidths=[3*cm,14*cm])

    def set_sender(self,name,address,email):
        self.sender_name = name
        self.sender_address = [ name ] + \
            address.splitlines() + \
            [ "E-Mail: " + email ]

    def set_auftraggeber(self,auftraggeber):
        self.recipient_address = [ auftraggeber.name ] + \
            auftraggeber.address.splitlines() + \
            [ "E-Mail: " + auftraggeber.email]

    def set_add_info(self,add_info):
        self.add_info = add_info

    def set_relevant_apps(self,apps):
        table_style = TableStyle([
                ('VALIGN',(0,0),(0,-1),'TOP')
            ])

        list_apps = [
            [Paragraph(x.number,styles['Message']),
            Paragraph(x.description,styles['Message'])] for x in apps]

        self.table_apps = Table(list_apps,colWidths=[3*cm,14*cm])
        self.table_apps.setStyle(table_style)

    def pdf_response(self):
        # create document structure
        document = Document(
            sender = self.sender_address,
            recipient = self.recipient_address,
            date = datetime.datetime.now().strftime("%d.%m.%Y"),
            content = self._content()
        )

        # create response instance
        response = HttpResponse(content_type='application/pdf')
        filename = "dsg-2000-auskunft-" + self.sender_name.replace(' ','-').lower() + ".pdf"
        response['Content-Disposition'] = \
            'attachment; filename="' + filename + '"'

        # build letter template
        buff = BytesIO()
        template = BriefTemplate(buff, document)
        template.build(document.content)
        pdf_response = buff.getvalue()
        buff.close()

        response.write(pdf_response)
        return response

    def _content(self):
        # TODO: move styles somewhere else
        # style for additional information box
        ibs = ParagraphStyle('inputBoxStyle',styles['Message'])
        ibs.fontName = 'Courier'
        ibs.leftIndent = cm
        ibs.spaceBefore = 0.2*cm
        ibs.spaceAfter = 0.5*cm
        # font style for letter subject
        styles['Subject'].fontName = 'Helvetica-Bold'

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
            self.table_apps,
            Paragraph(_("auskunft_registered_application_post"),styles['Message']),


            Paragraph(_("auskunft_additional_info_text"), styles['Message']),
            Paragraph(self.add_info,ibs),

            Paragraph(_("auskunft_method_identity"),styles['Message']),
            Paragraph(_("auskunft_expected_response"),styles['Message']),

            Spacer(0,0.5*cm),
            Paragraph(_("auskunft_signature"),styles['Signature']),
            Paragraph(self.sender_name,styles['Signature']),
        ]

        return content
