import logging
from nettraversal.utils.nftool import NetForwardManager, SocatNetForwardController
from nettraversal.utils.portpool import PortPool
from nettraversal.models import NetForward
import config
import sys

logger = logging.getLogger(__name__)

logger.info("Net Traversal's Net Forward Service seting up...")


nfportpool_range = (50000, 60000)
nf_ip_binding = "127.0.0.1"

if hasattr(config, "NET_FORWARD_PORT_RANGE"):
    nfportpool_range = config.NET_FORWARD_PORT_RANGE

if hasattr(config, "NET_FORWARD_IP_BINDING"):
    nf_ip_binding = config.NET_FORWARD_IP_BINDING


# net forward port pool
nfportpool = PortPool(*nfportpool_range)
# net forward manager
nfmanager = NetForwardManager(controller_class=SocatNetForwardController)


if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    # setup net forward
    for nf in NetForward.objects.all():
        if nf.forward_port is None:
            nf.forward_port = nfportpool.allocate()
            nf.save()
        nfmanager.add_forwarding_controller(
            id=nf.pk,
            src_ip=nf.origin_ip,
            src_port=nf.origin_port,
            src_protocal=nf.origin_protocol,
            dst_ip=nf_ip_binding,
            dst_port=nf.forward_port,
        )
        if nf.is_active:
            nfmanager.start_forwarding(nf.pk)

logger.info("Net Traversal's Net Forward Service setup finished...")
