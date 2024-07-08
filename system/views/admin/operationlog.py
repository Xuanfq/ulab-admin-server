
from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet, PkMultipleFilter
from common.core.modelset import ListDeleteModelSet, OnlyExportDataAction
from system.models import OperationLog
from system.utils.serializer import OperationLogSerializer


class OperationLogFilter(BaseFilterSet):
    ipaddress = filters.CharFilter(field_name='ipaddress', lookup_expr='icontains')
    system = filters.CharFilter(field_name='system', lookup_expr='icontains')
    browser = filters.CharFilter(field_name='browser', lookup_expr='icontains')
    path = filters.CharFilter(field_name='path', lookup_expr='icontains')

    # 自定义的搜索模板，需要前端同时添加 userinfo 类型
    creator_id = PkMultipleFilter(input_type='search-users')

    class Meta:
        model = OperationLog
        fields = ['module', 'ipaddress', 'system', 'creator_id', 'browser', 'path', 'created_time']


class OperationLogView(ListDeleteModelSet, OnlyExportDataAction):
    """
    用户操作日志
    User Action/Operation Log
    """
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer

    ordering_fields = ['created_time', 'updated_time']
    filterset_class = OperationLogFilter
