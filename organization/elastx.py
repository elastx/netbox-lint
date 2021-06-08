#!/usr/bin/env python3
"""Elastx specific configuration."""
import pynetbox
import requests
from requests_toolbelt.adapters import host_header_ssl

from linter import util


def netbox_api(token: str) -> pynetbox.core.api.Api:
    """Return a new Netbox API connection API object."""
    ses = requests.Session()
    ses.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    ses.headers = {'Host': 'netbox.s.elx.io'}
    netbox = pynetbox.api('https://localhost:32337', token=token)
    netbox.http_session = ses
    return netbox


def rule_settings() -> util.RuleSettings:
    """Return organization specific rule settings."""
    return {}
