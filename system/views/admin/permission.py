import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet
from common.core.modelset import BaseModelSet, ImportExportDataAction
from system.models import DataPermission
from system.utils.serializer import DataPermissionSerializer

logger = logging.getLogger(__name__)


class DataPermissionFilter(BaseFilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = DataPermission
        fields = ['pk', 'name', 'mode_type', 'is_active', 'description']


class DataPermissionView(BaseModelSet, ImportExportDataAction):
    """
    数据权限管理
    Data Permission Management
    """
    queryset = DataPermission.objects.all()
    serializer_class = DataPermissionSerializer
    ordering_fields = ['created_time']
    filterset_class = DataPermissionFilter
