"""Netbox linting rules for Devices."""
# pylint: disable=C0116 (missing-function-docstring)
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
        if device.name is None:
            yield 'Device has no name'
            return
        if not re.match(r'[a-z0-9-]+', device.name):
            yield 'Name contains invalid characters'
        if len(device.name) < 3:
            yield 'Name is too short'

class DeviceLocationRule:
    """Ensure that device location is sane."""
    ID = 'DEVICE-LOCATION'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Iterator[str]:
        if device.site['id'] is None:
            yield 'Device must be located in a site'

class DeviceAssetTagRule:
    """Ensure that device has an asset tag."""
    ID = 'DEVICE-ASSETTAG'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Iterator[str]:
        if device.asset_tag is None:
            yield 'Device must have an asset tag'

class DevicePrimaryIPRule:
    """Ensure that specified device has primary ip set."""
    ID = 'DEVICE-PRIMARYIP'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Iterator[str]:
        if device.device_role['name'] in ("Compute", "HSM","Storage", "Network"):
            if device.primary_ip is None:
                yield 'Devices with role "{}" must have a primary IP'.format(
                    device.device_role['name'])

class DeviceLifecycleRule:
    """Ensure that device lifecycle state."""
    ID = 'DEVICE-LIFECYCLE'

    def __init__(self, settings: util.RuleSetting):
        pass

    def check(self, device: pynetbox.models.dcim.Devices) -> Iterator[str]:
        if device.device_role['name'] == "Compute":
            if device.status['value'] == "staged":
                if device.platform is not None:
                    yield 'Devices with status "staged" should not be assigned a platform'
            if device.status['value'] == "active":
                if device.platform is None:
                    yield 'Devices with status "active" should be assigned a platform'

AllRules = [
    DeviceNamingRule,
    DeviceLocationRule,
    DeviceAssetTagRule,
    DevicePrimaryIPRule,
    DeviceLifecycleRule
]
