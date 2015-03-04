# provisioning

A library to manage Apple's provisioning profiles.

---

# Install

    python setup.py install

> Note: `pyOpenSSL` and `pyasn1` are required.

    pip install -r requirements.txt

# API

## Example

    #!/usr/bin/env python
    
    from provisioning.profile import ProvisioningProfile
    from provisioning.entitlements import Entitlements
    
    provisioning_profile = ProvisioningProfile(data)
    entitlements = provisioning_profile.entitlements

## Pydoc

To get more information, see API docs.

    pydoc provisioning

## Sphinx

Or to build a fancy HTML API document, type below in a terminal.

    cd docs
    make html

Then open [html](docs/_build/html/index.html) in a web browser.

# Testing

To run unit tests, you should overwrite [test.mobileprovision](tests/test.mobileprovision).

> Note: `test.mobileprovision` skips git worktree (see `man git-update-index`).

Then run:

    python tests -v

# License

This program is licensed under [the MIT License](LICENSE.txt).

