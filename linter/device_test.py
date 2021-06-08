"""Test for Netbox linting rules for Devices."""
# pylint: disable=C0116 (missing-function-docstring)
from collections import namedtuple
import unittest

from . import device as rules


class FakeDevice(namedtuple(
    'FakeDevice', ['name', 'status', 'device_role', 'platform', 'asset_tag', 'site', 'primary_ip'],
    defaults=['Fake', {'value': 'toaster'}, {'name': 'Invalid'}, 'Fake', None, None, None])):
    """A fake device replicating the Netbox Device model."""


class TestDeviceNamingRule(unittest.TestCase):
    """Tests the behavior of the DeviceNamingRule check."""

    def test_invalid_chars(self):
        rule = rules.DeviceNamingRule({})
        device = FakeDevice(name='Fake')
        got = list(rule.check(device))
        self.assertCountEqual(got, [
            'Name contains invalid characters',
        ])

    def test_too_short_name(self):
        rule = rules.DeviceNamingRule({})
        device = FakeDevice(name='f1')
        got = list(rule.check(device))
        self.assertCountEqual(got, [
            'Name is too short',
        ])

class TestDeviceLocationRule(unittest.TestCase):
    """Tests the behavior of the DeviceLocationRule check."""

    def test_with_site_name(self):
        rule = rules.DeviceLocationRule({})
        device = FakeDevice(site={'id': '1'})
        got = list(rule.check(device))
        self.assertCountEqual(got, [])

class TestDeviceAssetTagRule(unittest.TestCase):
    """Tests the behavior of the DeviceAssetTagRule check."""

    def test_without_asset_tag(self):
        rule = rules.DeviceAssetTagRule({})
        device = FakeDevice()
        got = list(rule.check(device))
        self.assertCountEqual(got, [
            'Device must have an asset tag',
        ])

    def test_with_valid_asset_tag(self):
        rule = rules.DeviceAssetTagRule({})
        device = FakeDevice(asset_tag='000001')
        got = list(rule.check(device))
        self.assertCountEqual(got, [])


class TestDevicePrimaryIPRule(unittest.TestCase):
    """Tests the behavior of the DevicePrimaryIPRule check."""

    def test_invalid_role(self):
        rule = rules.DevicePrimaryIPRule({})
        device = FakeDevice()
        got = list(rule.check(device))
        self.assertCountEqual(got, [])

    def test_invalid_primaryip(self):
        rule = rules.DevicePrimaryIPRule({})
        device = FakeDevice(device_role={'name': 'Compute'})
        got = list(rule.check(device))
        self.assertCountEqual(got, [
            'Devices with role "Compute" must have a primary IP',
        ])

    def test_valid(self):
        rule = rules.DevicePrimaryIPRule({})
        device = FakeDevice(device_role={'name': 'Compute'}, primary_ip="10.10.10.0/24")
        got = list(rule.check(device))
        self.assertCountEqual(got, [])


class TestDeviceLifecycleRule(unittest.TestCase):
    """Tests the behavior of the DeviceLifecycleRule check."""

    def test_valid_compute_platform(self):
        rule = rules.DeviceLifecycleRule({})
        device = FakeDevice(
            status={'value': 'active'},device_role={'name': 'Compute'})
        got = list(rule.check(device))
        self.assertCountEqual(got, [])

    def test_missing_compute_platform(self):
        rule = rules.DeviceLifecycleRule({})
        device = FakeDevice(
            status={'value': 'active'},device_role={'name': 'Compute'},platform=None)
        got = list(rule.check(device))
        self.assertCountEqual(got, [
            'Devices with status "active" should be assigned a platform',
        ])

    def test_valid_compute_staged_platform(self):
        rule = rules.DeviceLifecycleRule({})
        device = FakeDevice(
            status={'value': 'staged'},device_role={'name': 'Compute'},platform=None)
        got = list(rule.check(device))
        self.assertCountEqual(got, [])

    def test_missing_compute_staged_platform(self):
        rule = rules.DeviceLifecycleRule({})
        device = FakeDevice(
            status={'value': 'staged'},device_role={'name': 'Compute'})
        got = list(rule.check(device))
        self.assertCountEqual(got, [
            'Devices with status "staged" should not be assigned a platform',
        ])

if __name__ == '__main__':
    unittest.main()
