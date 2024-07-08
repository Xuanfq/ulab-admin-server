

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet, PkMultipleFilter
from common.core.modelset import ListDeleteModelSet, OnlyExportDataAction
from system.models import UserLoginLog
from system.utils.serializer import UserLoginLogSerializer


class UserLoginLogFilter(BaseFilterSet):
    ipaddress = filters.CharFilter(field_name='ipaddress', lookup_expr='icontains')
    system = filters.CharFilter(field_name='system', lookup_expr='icontains')
    browser = filters.CharFilter(field_name='browser', lookup_expr='icontains')
    agent = filters.CharFilter(field_name='agent', lookup_expr='icontains')
    creator_id = PkMultipleFilter(input_type='search-users')

    class Meta:
        model = UserLoginLog
        fields = ['login_type', 'ipaddress', 'system', 'creator_id', 'browser', 'agent', 'created_time']


class UserLoginLogView(ListDeleteModelSet, OnlyExportDataAction):
    """
    用户登录日志
    User login logs
    """
    queryset = UserLoginLog.objects.all()
    serializer_class = UserLoginLogSerializer

    ordering_fields = ['created_time']
    filterset_class = UserLoginLogFilter
