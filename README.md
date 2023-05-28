# Airbolt API Client

A limited client for the Airbolt API that provides information about their GPS trackers, reverse engineered from their web UI.

## Features
* login with username and password (no 2FA)
* fetch device list
* get device location history

## Example
```python

from airbolt_api import AirboltClient


def run():
    client = AirboltClient("username", "password")
    client.login()
    for device in client.find_devices():
        history = client.get_device_history_page(device.device_uuid, page=1, page_size=10)
        print(f" * {device.name} at {history.data[0].address} on {history.data[0].time_created}")

```