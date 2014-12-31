#! /usr/bin/env python
import sys
import django
from auskunft.dvr import DVR
from auskunft.models import Auftraggeber, Category, Membership, Application
import datetime

d = DVR()
django.setup()

for dvr in sys.stdin.readlines():
    # lookup dvr number
    details = d.details(dvr[:7])
    if not details:
        continue
    # add auftraggeber
    ag = Auftraggeber(name=details[0],address=details[1],email=details[2],dvr=int(dvr))
    ag.save()

    # add all applications for this auftraggeber
    new_dvr = "{0:07d}".format(ag.dvr)
    ag_apps = d.applications(new_dvr)
    if ag_apps == None:
        continue
    for ag_app in ag_apps:
        try:
            dt = datetime.datetime.strptime(ag_app[2],'%d.%m.%Y')
        except:
            continue
        new_date = "{0}-{1}-{2}".format(dt.year,dt.month,dt.day)
        aam = Application(number=ag_app[0],description=ag_app[1],date=new_date,state=ag_app[3])
        aam.auftraggeber = ag
        aam.save()
    # debug output
    print details[0] + " (" + str(len(ag_apps)) + ")"

