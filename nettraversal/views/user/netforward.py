import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet, CreatorUserFilter
from common.core.modelset import BaseModelSet, ImportExportDataAction, OwnerModelSet
from nettraversal.models import NetForward
from nettraversal.utils.serializer import NetForwardUserSerializer

logger = logging.getLogger(__name__)


class NetForwardUserFilter(BaseFilterSet, CreatorUserFilter):
    src_ip = filters.CharFilter(field_name="dst_ip", lookup_expr="icontains")

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


class NetForwardUserView(BaseModelSet, ImportExportDataAction, OwnerModelSet):
    """
    网络转发
    Network Forwarding
    """

    serializer_class = NetForwardUserSerializer
    ordering_fields = ["created_time"]
    filterset_class = NetForwardUserFilter
    
    def get_queryset(self):
        return NetForward.objects.filter(creator=self.request.user.pk)
    

