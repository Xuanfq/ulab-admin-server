import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet, CreatorUserFilter
from common.core.modelset import BaseModelSet, ImportExportDataAction
from net.models import PortForward
from net.serializers.portforward import PortForwardAdminSerializer
from net.services import pfservice

logger = logging.getLogger(__name__)


class PortForwardAdminFilter(BaseFilterSet, CreatorUserFilter):
    dst_ip = filters.CharFilter(field_name="dst_ip", lookup_expr="icontains")

    class Meta:
        model = PortForward
        fields = [
            "dst_ip",
            "dst_port",
            "protocol",
            "is_active",
            "src_port",
            "created_time",
        ]  # Fields are used for front-end automatic generation of search forms


class PortForwardAdminView(BaseModelSet, ImportExportDataAction):
    """
    网络转发
    Network Forwarding
    """

    queryset = PortForward.objects.all()
    serializer_class = PortForwardAdminSerializer
    ordering_fields = ["created_time"]
    filterset_class = PortForwardAdminFilter

    def perform_destroy(self, instance):
        pfservice.remove(instance.pk)
        return super().perform_destroy(instance)
