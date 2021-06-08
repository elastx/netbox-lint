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

Before submitting a pull request, run `make codelint` to see if there are any
issues with the written code.
