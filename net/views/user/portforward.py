import logging

from django_filters import rest_framework as filters
from django.utils.translation import gettext as _
from common.core.filter import BaseFilterSet, CreatorUserFilter
from common.core.modelset import BaseModelSet, ImportExportDataAction, OwnerModelSet
from net.models import PortForward
from net.utils.serializer import PortForwardUserSerializer
from common.base.magic import cache_response
from common.base.utils import get_choices_dict
from common.core.response import ApiResponse
from net.services import pfservice

logger = logging.getLogger(__name__)


class PortForwardUserFilter(BaseFilterSet, CreatorUserFilter):
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


class PortForwardUserView(BaseModelSet, ImportExportDataAction):
    """
    网络转发
    Network Forwarding
    """

    serializer_class = PortForwardUserSerializer
    ordering_fields = ["created_time"]
    filterset_class = PortForwardUserFilter

    def perform_destroy(self, instance):
        pfservice.remove(instance.pk)
        return super().perform_destroy(instance)

    def get_queryset(self):
        self.queryset = PortForward.objects.filter(creator=self.request.user.pk)
        return self.queryset

    def get_cache_key(self, view_instance, view_method, request, args, kwargs):
        func_name = f"{view_instance.__class__.__name__}_{view_method.__name__}"
        return f"{func_name}_{request.user.pk}"

    @cache_response(timeout=600, key_func="get_cache_key")
    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        return ApiResponse(
            **data, choices_dict=get_choices_dict(PortForward.ProtocolChoices.choices)
        )
