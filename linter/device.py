"""Netbox linting rules for Devices."""
import typing
import pynetbox
from typing import Optional

from . import util


class DeviceNamingRule:
    ID = 'DEVICE-NAME'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Optional[str]:
        if device.name == '70037B1':
            return 'Name is banned'
        return None


AllRules = [
        DeviceNamingRule
]


