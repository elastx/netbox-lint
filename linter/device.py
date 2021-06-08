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

class DeviceLocationRule:
    ID = 'DEVICE-LOCATION'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Iterator[str]:
        if device.site['id'] is None:
            yield 'Device must be located in a site'

class DeviceAssetTagRule:
    ID = 'DEVICE-ASSETTAG'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Iterator[str]:
        if device.asset_tag is None:
            yield 'Device must have an asset tag'


class DevicePrimaryIPRule:
    ID = 'DEVICE-PRIMARYIP'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Iterator[str]:
        if device.device_role['name'] == "Compute":
            if device.primary_ip is None:
                yield 'Devices with status "active" must have a primary IP'
            if device.status['value'] == "staged":
                if device.platform is not None:
                    yield 'Devices with status "staged" should not be assigned a platform'
            if device.status['value'] == "active":
                if device.platform is None:
                    yield 'Devices with status "active" should not be assigned a platform'  
        if device.device_role['name'] == "HSM":
            if device.primary_ip is None:
                yield 'Devices with status "active" must have a primary IP'
        if device.device_role['name'] == "Storage":
            if device.primary_ip is None:
                yield 'Devices with status "active" must have a primary IP'
        if device.device_role['name'] == "Network":
            if device.primary_ip is None:
                yield 'Devices with status "active" must have a primary IP' 

class DeviceStatusRule:
    ID = 'DEVICE-STATUS'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Iterator[str]:
        if device.device_role['name'] == "Compute":
            if device.status['value'] == "staged":
                if device.platform is not None:
                    yield 'Devices with status "staged" should not be assigned a platform'
            if device.status['value'] == "active":
                if device.platform is None:
                    yield 'Devices with status "active" should not be assigned a platform'  

AllRules = [
    DeviceNamingRule,
    DeviceLocationRule,
    DeviceAssetTagRule,
    DevicePrimaryIPRule,
    DeviceStatusRule
]
