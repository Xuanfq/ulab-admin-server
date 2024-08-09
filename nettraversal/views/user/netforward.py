import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet, CreatorUserFilter
from common.core.modelset import BaseModelSet, ImportExportDataAction, OwnerModelSet
from nettraversal.models import NetForward
from nettraversal.utils.serializer import NetForwardUserSerializer
from common.base.magic import cache_response
from common.base.utils import get_choices_dict
from common.core.modelset import OwnerModelSet
from common.core.response import ApiResponse

logger = logging.getLogger(__name__)


class NetForwardUserFilter(BaseFilterSet, CreatorUserFilter):
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


class NetForwardUserView(BaseModelSet, ImportExportDataAction, OwnerModelSet):
    """
    网络转发
    Network Forwarding
    """

    serializer_class = NetForwardUserSerializer
    ordering_fields = ["created_time"]
    filterset_class = NetForwardUserFilter

    def get_queryset(self):
        self.queryset = NetForward.objects.filter(creator=self.request.user.pk)
        return self.queryset

    def get_cache_key(self, view_instance, view_method, request, args, kwargs):
        func_name = f"{view_instance.__class__.__name__}_{view_method.__name__}"
        return f"{func_name}_{request.user.pk}"

    @cache_response(timeout=600, key_func="get_cache_key")
    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        return ApiResponse(
            **data, choices_dict=get_choices_dict(NetForward.ProtocolChoices.choices)
        )
