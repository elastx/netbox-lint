# netbox-lint
Rule checker for Netbox to enforce naming and associations

## Usage

```
# Make sure you have Python 3.9 or newer
$ apt install python3.9 python3.9-venv
$ make
# Make sure you have the Pomerium tunnel up before running
$ NETBOX_TOKEN="$(<~/.netbox-token)" ./netboxlint -o elastx
```


## Development

To add a new rule, add it under e.g. `linter/device.py` and make sure to
add it to the AllRules array in the end.

You can add tests to ensure that your check is correct to e.g. `linter/device_test.py`.
To run the tests run `make check`.

Before submitting a pull request, run `make codelint` to see if there are any
issues with the written code.
