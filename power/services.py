import logging
import sys
from common.management.commands.services.services.appd import (
    SecureSocketAppService,
    SecureSocketAppClient,
)
from power.utils.power import ApcPduPowerControllerManager
import config

logger = logging.getLogger(__name__)


host = "127.0.0.1"
port = 9002
key = "qwertyuiasdfghjk"
username = "ApcPduPowerService"
password = "ApcPduPowerService"


class ApcPduPowerService(SecureSocketAppService):
    def __init__(self):
        super().__init__()
        self.manager = ApcPduPowerControllerManager()

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
        try:
            if reqcmd == "add":
                self.manager.add(**kwargs)
            elif reqcmd == "remove":
                self.manager.remove(**kwargs)
            elif reqcmd == "alive":
                alive = self.manager.alive(**kwargs)
                res_args.append(alive)
            elif reqcmd == "power_status":
                status = self.manager.power_status(**kwargs)
                res_args.append(status)
            elif reqcmd == "power_on":
                status = self.manager.power_on(**kwargs)
                res_args.append(status)
            elif reqcmd == "power_off":
                status = self.manager.power_off(**kwargs)
                res_args.append(status)
            elif reqcmd == "power_reboot":
                status = self.manager.power_reboot(**kwargs)
                res_args.append(status)
        except Exception as e:
            res_args.extend([False, str(e)])
        return res_args, res_kwargs


class ApcPduPowerClient(SecureSocketAppClient):
    def __init__(self, host, port, username, password, key):
        super().__init__(host, port, username, password, key)

    def add(
        self,
        id: str | int,
        ip,
        port,
        username,
        password,
    ):
        flag, args, kwargs = self.send_request(
            "add",
            **{
                "id": str(id),
                "ip": ip,
                "port": port,
                "username": username,
                "password": password,
            },
        )
        if flag:
            return True, None
        else:
            return False, args[0]

    def remove(self, id: str | int):
        flag, args, kwargs = self.send_request("remove", **{"id": str(id)})
        if flag:
            return True, None
        else:
            return False, args[0]

    def alive(self, id: str | int):
        flag, args, kwargs = self.send_request("alive", **{"id": str(id)})
        if flag:
            return args[0], None
        else:
            return False, args[0]

    def power_status(self, id: str | int, outlet: str | int, cache: bool = True):
        flag, args, kwargs = self.send_request(
            "power_status", **{"id": str(id), "outlet": str(outlet), "cache": cache}
        )
        if flag:
            return args[0], None
        else:
            return False, args[0]

    def power_on(self, id: str | int, outlet: str | int, delay: int = 0):
        flag, args, kwargs = self.send_request(
            "power_on", **{"id": str(id), "outlet": str(outlet), "delay": delay}
        )
        if flag:
            return args[0], None
        else:
            return False, args[0]

    def power_off(self, id: str | int, outlet: str | int, delay: int = 0):
        flag, args, kwargs = self.send_request(
            "power_off", **{"id": str(id), "outlet": str(outlet), "delay": delay}
        )
        if flag:
            return args[0], None
        else:
            return False, args[0]

    def power_reboot(
        self, id: str | int, outlet: str | int, delay: int = 0, interval=5
    ):
        flag, args, kwargs = self.send_request(
            "power_reboot",
            **{
                "id": str(id),
                "outlet": str(outlet),
                "delay": delay,
                "interval": interval,
            },
        )
        if flag:
            return args[0], None
        else:
            return False, args[0]


apservice = ApcPduPowerClient(
    host=host, port=port, username=username, password=password, key=key
)


def setup():
    if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
        logger.info("Power's APC PDU Power Service loading...")
        from power.models import ApcPduPower

        for ap in ApcPduPower.objects.all():
            if ap.is_active:
                apservice.add(
                    id=ap.pk,
                    ip=ap.ip,
                    port=ap.port,
                    username=ap.username,
                    password=ap.password,
                )
        logger.info("Power's APC PDU Power Service loading finished...")


setup()
