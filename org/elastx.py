#!/usr/bin/env python3
"""Elastx specific configuration."""
import pynetbox
import requests
from requests_toolbelt.adapters import host_header_ssl


class Elastx:
    def new_connection(self, token):
        s = requests.Session()
        s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
        s.headers = {'Host': 'netbox.s.elx.io'}
        nb = pynetbox.api('https://localhost:32337', token=token)
        nb.http_session = s
        return nb

    def rules(self):
        return {}
