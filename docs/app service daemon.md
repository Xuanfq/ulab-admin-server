# app service daemon

Each Django app will be created multiple times, that is, multiple workers will be created to improve throughput. Therefore, there will be no singular case. This will result in the need to use third-party services in resource constrained situations (such as having 12 workers but only supporting 5 external service connections), such as producer consumer mode.

To this end, provide lightweight app microservice daemon processes.

## How to use

1. Add `app/services.py` to the app directory.
2. Inherit and implement this class `AppServiceBase` (or it's subclasses) from `common.management.commands.services.services.appd`
3. Communicating through processes or networks, `socket` is recommended. `SecureSocketAppService` and `SecureSocketAppClient` are examples of secure socket communication.

- Notice: The corresponding socket connection or inter process communication must use lazy loading, otherwise an error will be reported.

## Example

```python
# services.py
from common.management.commands.services.services.appd import (
    SecureSocketAppService,
    SecureSocketAppClient,
)

host = "127.0.0.1"
port = 9001
key = "qwertyuiasdfghjk"
username = "PowerService"
password = "PowerService"


class PowerService(SecureSocketAppService):
    def __init__(self):
        super().__init__()

    @property
    def host(self):
        return host

    @property
    def port(self):
        return port

    @property
    def key(self):
        return key

    @property
    def username(self):
        return username

    @property
    def password(self):
        return password

    def handle_request(self, reqcmd, *args, **kwargs):
        res_args, res_kwargs = [], {}
        if reqcmd == "poweron":
            outlet = args[0]
            # TODO: power on outlet
            pass
        # ...
        return res_args, res_kwargs


class PowerClient(SecureSocketAppClient):
    def __init__(self, host, port, username, password, key):
        super().__init__(host, port, username, password, key)


powerclient = PowerClient(
    host=host, port=port, username=username, password=password, key=key
)

# serializer.py
class xxx:
    def poweron(self, validated_data)
        outlet  = validated_data.get("outlet", None)
        if outlet:
            powerclient.send_request("poweron", outlet)
```
