"""Test for Netbox linting rules for Devices."""
# pylint: disable=C0116 (missing-function-docstring)
from collections import namedtuple
import unittest

from . import device as rules


class FakeDevice(namedtuple(
    'FakeDevice', ['name', 'status', 'device_role', 'platform'],
    defaults=['Fake', {'value': 'toaster'}, {'name': 'Invalid'}, 'Fake'])):
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
