from django.shortcuts import render

import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet
from common.core.modelset import BaseModelSet, ImportExportDataAction
from nettraversal.models import NetForward
from nettraversal.utils.serializer import NetForwardSerializer

logger = logging.getLogger(__name__)


class NetForwardFilter(BaseFilterSet):

    class Meta:
        model = NetForward
        fields = [
            "creator",
            "origin_ip",
            "origin_port",
            "origin_protocol",
            "forward_ip",
            "forward_port",
            "created_time",
        ]  # Fields are used for front-end automatic generation of search forms


class NetForwardView(BaseModelSet, ImportExportDataAction):
    """
    网络转发
    Network Forwarding
    """
    
    queryset = NetForward.objects.all()
    serializer_class = NetForwardSerializer
    ordering_fields = ["created_time"]
    filterset_class = NetForwardFilter
