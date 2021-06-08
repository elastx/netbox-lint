"""The Netbox linter."""
# pylint: disable=R0903 (too-few-public-methods)
from typing import Iterator
import pynetbox

from . import device
from . import util


rules = device.AllRules


class LintResult:
    """Represents a found linting issue."""

    # TODO: Typing using protocols
    def __init__(self, check, record, msg: str):
        self.check = check
        self.msg = msg
        self.record = record

    def __str__(self):
        return '{}: ID={}, Name={}: {}'.format(
                self.check.ID,
                self.record.id,
                self.record.name,
                self.msg)


class Linter:
    """The Netbox linter.

    Note: the linter is stateful and the rule instances are saved between runs.
    If you implement a check for e.g. unique names, make sure to save the record
    ID to allow for subsequent runs that ignore hits on itself.
    """

    def __init__(self, rulesettings: util.RuleSettings):
        # Create all rule objects, allow them to create state stores or whatever
        # they might need
        self.rules = []
        for rc in rules:
            settings = rulesettings.get(rc.ID, {})
            self.rules.append(rc(settings))

    def lint(self, recordset: pynetbox.core.response.RecordSet) -> Iterator[LintResult]:
        """Lint a given Netbox RecordSet."""
        for rule in self.rules:
            for record in recordset:
                for res in rule.check(record):
                    yield LintResult(rule, record, res)
