"""
Tests the JobConstructor
"""

import pytest

from controllers.dock.runner import JobConstructor

PAYLOAD = {
    "deploy": {
        "dev": {
            "auto-build": {
                "buildpack": "",
                "name": "myimage:dev"
            },
            "image": "debian:stable-slim",
            "script": [
                "echo hi",
                "echo finished job!"
            ]
        }
    }
}

OUTPUT = {
    "payload": {
        "jobs": [
            {
                "name": "deploy",
                "stages": [
                    {
                        "name": "dev",
                        "auto-build": {
                            "buildpack": "",
                            "name": "myimage:dev"
                        },
                        "image": "debian:stable-slim",
                        "script": [
                            "echo hi",
                            "echo finished job!"
                        ]
                    }
                ]
            }
        ]
    }
}

@pytest.fixture(scope='function')
def constructor():
    return JobConstructor(PAYLOAD)

def test_constructor_can_create_payload(constructor):
    payload = constructor._create_payload()
    assert payload == OUTPUT

