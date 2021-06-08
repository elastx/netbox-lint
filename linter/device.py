"""Netbox linting rules for Devices."""
import typing
import pynetbox
import re
from typing import Iterator

from . import util


class DeviceNamingRule:
    ID = 'DEVICE-NAME'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Iterator[str]:
        if device.name is None:
            yield 'Device has no name'
            return
        if not re.match(r'[a-z0-9-]+', device.name):
            yield 'Name contains invalid characters'
        if len(device.name) < 3:
            yield 'Name is too short'


AllRules = [
        DeviceNamingRule
]


