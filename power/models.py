from django.db import models
from common.core.models import DbUuidModel, DbAuditModel
from django.utils.translation import gettext as _


# Create your models here.
class ApcPduPower(DbUuidModel, DbAuditModel):
    class OutletTypeChoices(models.IntegerChoices):
        OUTLET_8 = 8, _("8 Control Ports")
        OUTLET_24 = 24, _("24 Control Ports")

    name = models.CharField(unique=True, max_length=128, blank=False, help_text="name")
    type = models.IntegerField(
        choices=OutletTypeChoices, max_length=20, verbose_name=_("type")
    )
    ip = models.GenericIPAddressField(
        unique=True, null=False, blank=False, help_text="ip"
    )
    port = models.IntegerField(null=False, blank=False, verbose_name=_("port"))
    username = models.CharField(max_length=128, blank=False, help_text="username")
    password = models.CharField(max_length=128, blank=False, help_text="password")

    class Meta:
        unique_together = (("ip", "port"),)


class ApcPduPowerUnit(DbUuidModel, DbAuditModel):
    power = models.ForeignKey(ApcPduPower, on_delete=models.CASCADE)
    outlet = models.IntegerField(null=False, blank=False, help_text="outlet")
    status = models.CharField(
        null=False,
        blank=False,
        default="Unknown",
        max_length=128,
        help_text="power status",
    )

    class Meta:
        unique_together = (("power", "outlet"),)
