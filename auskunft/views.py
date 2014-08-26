from io import BytesIO
from reportlab.pdfgen import canvas
from django.shortcuts import render
from django.http import HttpResponse

from auskunft.forms import AuskunftForm

# Create your views here.
def index(request):
    form = AuskunftForm()
    return render(request,'auskunft/form.html',{'form':form})

def create(request):
    form = AuskunftForm(request.POST)
    if form.is_valid():
        # get data from form
        auftraggeber = form.cleaned_data['auftraggeber']
        name = form.cleaned_data['name']
        address = form.cleaned_data['address']
        email = form.cleaned_data['email']
        add_info = form.cleaned_data['additional_info']

        # open pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="auskunftbegehren.pdf"'
        buffer = BytesIO()

        # fill pdf
        p = canvas.Canvas(buffer)
        p.drawString(100,100,"Hello, World!")

        # save pdf and send it to client
        p.showPage()
        p.save()
        pdf = buffer.getValue()
        buffer.close()
        response.write(pdf)
        return response
