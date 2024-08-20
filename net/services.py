import logging
import sys
from common.management.commands.services.services.appd import (
    SecureSocketAppService,
    SecureSocketAppClient,
)
from net.utils.portpool import PortPool
from net.utils.portforward import SocatPortForwardController, PortForwardManager
import config

logger = logging.getLogger(__name__)


host = "127.0.0.1"
port = 9001
key = "qwertyuiasdfghjk"
username = "PortForwardService"
password = "PortForwardService"

pf_portpool_range = (50000, 60000)
pf_ip_binding = "127.0.0.1"

if hasattr(config, "NET_FORWARD_BINDING_PORT_RANGE"):
    pf_portpool_range = config.PORT_FORWARD_BINDING_PORT_RANGE

if hasattr(config, "NET_FORWARD_BINDING_IP"):
    pf_ip_binding = config.PORT_FORWARD_BINDING_IP


class PortForwardService(SecureSocketAppService):
    def __init__(self):
        # net forward manager
        self.manager = PortForwardManager(SocatPortForwardController)
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

    def stop(self):
        self.manager.remove_all_forwarding_controllers()
        return super().stop()

    def handle_request(self, reqcmd, *args, **kwargs):
        res_args, res_kwargs = [], {}
        try:
            if reqcmd == "add":
                flag = self.manager.add_forwarding_controller(**kwargs)
                res_args.append(flag)
            elif reqcmd == "remove":
                flag = self.manager.remove_forwarding_controller(kwargs["id"])
                res_args.append(flag)
        except Exception as e:
            res_args.extend([False, str(e)])
        return res_args, res_kwargs


class PortForwardClient(SecureSocketAppClient):
    def __init__(self, host, port, username, password, key):
        super().__init__(host, port, username, password, key)

    def add(
        self,
        id: str | int,
        src_ip: str,
        src_port: int,
        protocol: str,
        dst_ip: str,
        dst_port: int,
    ):
        flag, args, kwargs = self.send_request(
            "add",
            **{
                "id": str(id),
                "src_ip": src_ip,
                "src_port": src_port,
                "protocol": protocol,
                "dst_ip": dst_ip,
                "dst_port": dst_port,
            },
        )
        if flag:
            return args[0], None
        else:
            return False, args[0]

    def remove(self, id: str | int):
        flag, args, kwargs = self.send_request("remove", **{"id": str(id)})
        if flag:
            return args[0], None
        else:
            return False, args[0]


pfip = pf_ip_binding
pfportpool = PortPool(*pf_portpool_range)
pfservice = PortForwardClient(
    host=host, port=port, username=username, password=password, key=key
)


def setup():
    if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
        logger.info("Net's Port Forward Service loading...")
        # setup port forward
        from net.models import PortForward

        for nf in PortForward.objects.all():
            if nf.src_port is None:
                nf.src_port = pfportpool.allocate()
                nf.save()
            if nf.is_active:
                pfservice.add(
                    id=nf.pk,
                    src_ip=pfip,
                    src_port=nf.src_port,
                    protocol=nf.protocol,
                    dst_ip=nf.dst_ip,
                    dst_port=nf.dst_port,
                )
        logger.info("Net's Port Forward Service loading finished...")


setup()
