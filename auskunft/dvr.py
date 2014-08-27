#! /usr/bin/env python
import mechanize
from bs4 import BeautifulSoup

import sys

class DVR:
    def __init__(self):
        self.br = mechanize.Browser()

        self.br.open("https://dvr.dsb.gv.at")
        self.br.follow_link(text="ohne Anmeldung aufrufen")
        self.br.follow_link(text="DVR-Recherche")

    def _searchDVR(self,dvr):
        self.br.follow_link(text="DVR-Recherche")
        # search for dvr
        self.br.select_form(nr=0)
        self.br.form['ctl00$ContentHolder$DVRRechercheSuche$txtDVRNummer$txtDVRNummer_TextBox'] = dvr
        self.br.submit()

    def details(self,dvr):
        self._searchDVR(dvr)
        try:
            # get details
            self.br.select_form(nr=0)
            response = self.br.submit(name="ctl00$ContentHolder$DVRRechercheResult$btnDetail")
        except:
            return None

        # parse response
        soup = BeautifulSoup(response.read())
        detail_table = soup.find(summary="Zusammenfassung Daten des Auftraggebers")
        detail_data = detail_table.find_all('td')
        details = [x.contents[0].strip() for x in detail_data]

        name = details[1]
        address = details[2].replace(",","\r\n")
        email = details[4]
        return (name,address,email)

    def applications(self,dvr):
        self._searchDVR(dvr)
        try:
            # get details
            self.br.select_form(nr=0)
            response = self.br.submit(name="ctl00$ContentHolder$DVRRechercheResult$btnDAN")
        except:
            return None

        # parse response
        soup = BeautifulSoup(response.read())
        app_table = soup.find(id="ContentHolder_Datenanwendungen_GridDatenanwendungen")
        app_td = [x.contents[0] for x in app_table.find_all('td')]
        apps = zip(app_td[0::5],app_td[1::5],app_td[2::5],app_td[3::5],app_td[4::5])
        return [(x[1],x[2],x[3],x[4]) for x in apps]

if __name__ == "__main__":
    d = DVR()
    print d.applications(sys.argv[1])
