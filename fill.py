from auskunft.dvr import DVR
from auskunft.models import Auftraggeber, Category, Membership, Application
import datetime

d = DVR()

for ag in Auftraggeber.objects.all():
    ag_apps = d.applications(str(ag.dvr))
    for ag_app in ag_apps:
        dt = datetime.datetime.strptime(ag_app[2],'%d.%m.%Y')
        new_date = "{0}-{1}-{2}".format(dt.year,dt.month,dt.day)
        aam = Application(number=ag_app[0],description=ag_app[1],date=new_date,state=ag_app[3])
        aam.auftraggeber = ag
        aam.save()

