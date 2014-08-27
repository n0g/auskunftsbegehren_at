#! /usr/bin/env python
import mechanize

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
        # get details
        self.br.select_form(nr=0)
        response = self.br.submit(name="ctl00$ContentHolder$DVRRechercheResult$btnDetail")
        # TODO parse html
        print response.read()

    def applications(self,dvr):
        self._searchDVR(dvr)
        # get details
        self.br.select_form(nr=0)
        response = self.br.submit(name="ctl00$ContentHolder$DVRRechercheResult$btnDAN")
        # TODO parse html
        print response.read()

if __name__ == "__main__":
    d = DVR()
    d.applications("0000051")
