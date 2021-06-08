"""The Netbox linter."""
import pynetbox
from typing import Iterator

from . import device
from . import util


rules = device.AllRules


class LintResult:
    # TODO: Typing using protocols
    def __init__(self, check, record, msg: str):
        self.check = check
        self.msg = msg
        self.record = record

    def __str__(self):
        return '{}: {}: {}'.format(self.check.ID, self.record, self.msg)


class Linter:

    def __init__(self, rulesettings: util.RuleSettings):
        # Create all rule objects, allow them to create state stores or whatever
        # they might need
        self.rules = []
        for rc in rules:
            settings = rulesettings.get(rc.ID, {})
            self.rules.append(rc(settings))

    def lint(self, recordset: pynetbox.core.response.RecordSet) -> Iterator[LintResult]:
         # Run the check
        for r in self.rules:
            for record in recordset:
                res = r.check(record)
                if res:
                    yield LintResult(r, record, res)
