import django
from auskunft.models import Auftraggeber

django.setup()

for ag in Auftraggeber.objects.all():
    dvr = "{0:07d}".format(ag.dvr)
    print dvr
