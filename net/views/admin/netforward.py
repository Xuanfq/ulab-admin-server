import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet, CreatorUserFilter
from common.core.modelset import BaseModelSet, ImportExportDataAction
from net.models import NetForward
from net.utils.serializer import NetForwardAdminSerializer

logger = logging.getLogger(__name__)


class NetForwardAdminFilter(BaseFilterSet, CreatorUserFilter):
    dst_ip = filters.CharFilter(field_name="dst_ip", lookup_expr="icontains")

    class Meta:
        model = NetForward
        fields = [
            "dst_ip",
            "dst_port",
            "protocol",
            "is_active",
            "src_port",
            "created_time",
        ]  # Fields are used for front-end automatic generation of search forms


class NetForwardAdminView(BaseModelSet, ImportExportDataAction):
    """
    网络转发
    Network Forwarding
    """

    queryset = NetForward.objects.all()
    serializer_class = NetForwardAdminSerializer
    ordering_fields = ["created_time"]
    filterset_class = NetForwardAdminFilter
