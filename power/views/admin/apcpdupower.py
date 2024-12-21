import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet, CreatorUserFilter
from common.core.modelset import BaseModelSet, ImportExportDataAction
from power.models import ApcPduPower
from power.serializers.apcpdupower import ApcPduPowerAdminSerializer
from power.services import apservice

logger = logging.getLogger(__name__)


class ApcPduPowerAdminFilter(BaseFilterSet, CreatorUserFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    ip = filters.CharFilter(field_name="ip", lookup_expr="icontains")

    class Meta:
        model = ApcPduPower
        fields = [
            "name",
            "type",
            "ip",
            "created_time",
        ]  # Fields are used for front-end automatic generation of search forms


class ApcPduPowerAdminView(BaseModelSet, ImportExportDataAction):
    """
    APC PDU 电源控制器
    APC PDU Power
    """

    queryset = ApcPduPower.objects.all()
    serializer_class = ApcPduPowerAdminSerializer
    ordering_fields = ["created_time"]
    filterset_class = ApcPduPowerAdminFilter

    def perform_destroy(self, instance):
        apservice.remove(instance.id)
        return super().perform_destroy(instance)
