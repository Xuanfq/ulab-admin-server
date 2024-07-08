import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet, PkMultipleFilter
from common.core.modelset import BaseModelSet, ImportExportDataAction
from system.models import SystemConfig, UserPersonalConfig
from system.utils.modelset import InvalidConfigCacheAction
from system.utils.serializer import SystemConfigSerializer, UserPersonalConfigSerializer, \
    UserPersonalConfigExportImportSerializer

logger = logging.getLogger(__name__)


class SystemConfigFilter(BaseFilterSet):
    key = filters.CharFilter(field_name='key', lookup_expr='icontains')
    value = filters.CharFilter(field_name='value', lookup_expr='icontains')

    class Meta:
        model = SystemConfig
        fields = ['pk', 'is_active', 'key', 'inherit', 'access', 'value', 'description']


class SystemConfigView(BaseModelSet, InvalidConfigCacheAction, ImportExportDataAction):
    """
    系统配置管理
    System Configuration Management
    """
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer
    ordering_fields = ['created_time']
    filterset_class = SystemConfigFilter


class UserPersonalConfigFilter(SystemConfigFilter):
    username = filters.CharFilter(field_name='owner__username')
    owner_id = PkMultipleFilter(input_type='search-users')

    class Meta:
        model = UserPersonalConfig
        fields = ['pk', 'is_active', 'key', 'access', 'username', 'owner_id', 'value', 'description']


class UserPersonalConfigView(BaseModelSet, InvalidConfigCacheAction, ImportExportDataAction):
    """
    用户配置管理
    User Configuration Management
    """
    queryset = UserPersonalConfig.objects.all()
    serializer_class = UserPersonalConfigSerializer
    ordering_fields = ['created_time']
    filterset_class = UserPersonalConfigFilter
    import_data_serializer_class = UserPersonalConfigExportImportSerializer
    export_data_serializer_class = UserPersonalConfigExportImportSerializer
