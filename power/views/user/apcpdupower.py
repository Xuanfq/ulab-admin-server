import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet, CreatorUserFilter
from common.core.modelset import BaseModelSet, ImportExportDataAction, OwnerModelSet
from power.models import ApcPduPower
from power.serializers.apcpdupower import ApcPduPowerUserSerializer
from common.base.utils import get_choices_dict
from common.base.magic import cache_response
from common.core.response import ApiResponse
from power.services import apservice

logger = logging.getLogger(__name__)


class ApcPduPowerUserFilter(BaseFilterSet, CreatorUserFilter):
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


class ApcPduPowerUserView(BaseModelSet, ImportExportDataAction):
    """
    APC PDU 电源控制器
    APC PDU Power
    """

    serializer_class = ApcPduPowerUserSerializer
    ordering_fields = ["created_time"]
    filterset_class = ApcPduPowerUserFilter

    def get_queryset(self):
        self.queryset = ApcPduPower.objects.filter(creator=self.request.user.pk)
        return self.queryset

    def get_cache_key(self, view_instance, view_method, request, args, kwargs):
        func_name = f"{view_instance.__class__.__name__}_{view_method.__name__}"
        return f"{func_name}_{request.user.pk}"

    @cache_response(timeout=600, key_func="get_cache_key")
    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        return ApiResponse(
            **data, choices_dict=get_choices_dict(ApcPduPower.OutletTypeChoices.choices)
        )

    def perform_destroy(self, instance):
        apservice.remove(instance.id)
        return super().perform_destroy(instance)
