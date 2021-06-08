"""Netbox linting rules for Devices."""
# pylint: disable=R0201 (no-self-use)
# pylint: disable=R0903 (too-few-public-methods)
import re
from typing import Iterator
import pynetbox

from . import util


class DeviceNamingRule:
    """Ensure that device names are correctly formatted."""
    ID = 'DEVICE-NAME'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Iterator[str]:
        """Runs the check."""
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
