from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from common.core.models import DbUuidModel, DbAuditModel
from system.models import UserInfo


class PortForward(DbUuidModel, DbAuditModel):
    class ProtocolChoices(models.TextChoices):
        HTTP = "HTTP", _("HTTP")
        HTTPS = "HTTPS", _("HTTPS")
        RDP = "RDP", _("RDP")
        SSH = "SSH", _("SSH")
        TELNET = "TELNET", _("TELNET")
        TCP = "TCP", _("TCP")
        UDP = "UDP", _("UDP")

    src_ip = models.GenericIPAddressField(null=True, verbose_name=_("源地址"))
    src_port = models.IntegerField(null=True, verbose_name=_("源端口"))
    protocol = models.CharField(
        choices=ProtocolChoices, max_length=20, verbose_name=_("协议")
    )
    dst_ip = models.GenericIPAddressField(verbose_name=_("目标地址"))
    dst_port = models.IntegerField(verbose_name=_("目标端口"))
    is_active = models.BooleanField(default=False, verbose_name=_("是否启用该转发"))

    class Meta:
        verbose_name = _("端口转发")
        verbose_name_plural = _("端口转发")
