#! /usr/bin/env python
import sys
import datetime
import argparse

import django

from auskunft.dvr import DVR
from auskunft.models import Auftraggeber, Category, Membership, Application

def main():
    parser = argparse.ArgumentParser(description='Manage DVR Link')
    parser.add_argument('-d','--dvr', dest='dvr',help="DVR Number to look for")
    parser.add_argument('-s','--search', dest='search',help="Company Name to look for")
    args = parser.parse_args()

    d = DVR()
    django.setup()

    if args.dvr:
        # lookup
        details = d.details(args.dvr)
        apps = d.applications(args.dvr)

        # output
        print details[0]
        for a in apps:
            print a[0] + " " + a[1]

        # add to database
        a = Auftraggeber(name=details[0],address=details[1],email=details[2],dvr=args.dvr)
        a.save()
        for app in apps:
            dt = datetime.datetime.strptime(app[2],'%d.%m.%Y')
            new_date = "{0}-{1}-{2}".format(dt.year,dt.month,dt.day)
            new_app = Application(number=app[0],description=app[1],date=new_date,state=app[3])
            new_app.auftraggeber = a
            new_app.save()

        return
    if args.search:
        for c in d.searchCompany(args.search):
            print c[0] + " " + c[1]
        return

if __name__ == '__main__':
    sys.exit(main())

