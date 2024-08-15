import logging
from net.utils.nftool import (
    NetForwardManager,
    NetForwardManagerSingleton,
    SocatNetForwardController,
)
from net.utils.portpool import PortPool
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import sys
import config

logger = logging.getLogger(__name__)

logger.info("Net Traversal's Net Forward Service seting up...")


nfportpool_range = (50000, 60000)
nf_ip_binding = "127.0.0.1"

if hasattr(config, "NET_FORWARD_BINDING_PORT_RANGE"):
    nfportpool_range = config.NET_FORWARD_BINDING_PORT_RANGE

if hasattr(config, "NET_FORWARD_BINDING_IP"):
    nf_ip_binding = config.NET_FORWARD_BINDING_IP


# net forward port pool
nfportpool = PortPool(*nfportpool_range)
# net forward manager
nfmanager = NetForwardManagerSingleton(SocatNetForwardController)
logger.debug(f"nfmanager:{nfmanager} , size: {len(nfmanager)}")


# @receiver(post_migrate)
# def setup(sender, **kwargs):
def setup():
    if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
        logger.info("Net Traversal's Net Forward Service loading...")
        # setup net forward
        from net.models import NetForward

        for nf in NetForward.objects.all():
            if nf.src_port is None:
                nf.src_port = nfportpool.allocate()
                nf.save()
            if (
                nfmanager.add_forwarding_controller(
                    id=nf.pk,
                    src_ip=nf_ip_binding,
                    src_port=nf.src_port,
                    protocol=nf.protocol,
                    dst_ip=nf.dst_ip,
                    dst_port=nf.dst_port,
                )
                and nf.is_active
            ):
                nfmanager.start_forwarding(nf.pk)
        logger.debug(f"Net Forward Manager: {nfmanager} , size: {len(nfmanager)}")
        logger.info("Net Traversal's Net Forward Service loading finished...")


setup()

logger.info("Net Traversal's Net Forward Service setup finished...")
