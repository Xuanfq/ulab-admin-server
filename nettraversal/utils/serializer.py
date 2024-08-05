from common.core.serializers import (
    BaseModelSerializer,
    LabeledChoiceField,
    BasePrimaryKeyRelatedField,
)
from nettraversal import models
from django.utils.translation import gettext as _
from rest_framework import serializers
from nettraversal.netforward import nfmanager, nfportpool, nf_ip_binding
import logging

logger = logging.getLogger(__name__)


def to_common_protocol(protocol):
    if protocol in ["TCP", "SSH", "RDP", "HTTP", "HTTPS", "TELNET"]:
        return "TCP"
    elif protocol == models.NetForward.ProtocolChoices.UDP:
        return "UDP"
    else:
        return "TCP"


class NetForwardSerializer(BaseModelSerializer):
    class Meta:
        model = models.NetForward
        # The pk field is used for front-end deletion, update, and other identification purposes. If there is a deletion or update, the pk field must be added
        fields = [
            "pk",
            "creator",
            "origin_ip",
            "origin_port",
            "origin_protocol",
            "forward_ip",
            "forward_port",
            "is_active",
            "created_time",
            "updated_time",
        ]
        # Used for displaying table fields in the frontend
        table_fields = [
            "pk",
            "creator",
            "origin_ip",
            "origin_port",
            "origin_protocol",
            "forward_ip",
            "forward_port",
            "is_active",
        ]
        read_only_fields = ["pk", "forward_ip", "forward_port"]
        fields_unexport = ["pk"]  # Ignore this field when importing or exporting files

    creator = BasePrimaryKeyRelatedField(
        attrs=["pk", "username"], read_only=True, label=_("创建者")
    )
    origin_protocol = LabeledChoiceField(
        choices=models.NetForward.ProtocolChoices.choices,
        label=_("协议类型"),
    )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["forward_ip"] = nf_ip_binding
        return rep

    def create(self, validated_data):
        # add forward port
        port = nfportpool.allocate()
        validated_data["forward_port"] = port
        # create
        instance = super().create(validated_data)
        # add forwarding controller
        nfmanager.add_forwarding_controller(
            id=instance.pk,
            src_ip=instance.origin_ip,
            src_port=instance.origin_port,
            src_protocal=to_common_protocol(instance.origin_protocol),
            dst_ip=nf_ip_binding,
            dst_port=instance.forward_port,
        )
        if instance.is_active:
            nfmanager.start_forwarding(instance.pk)
        return instance

    def update(self, instance, validated_data):
        port = None
        if (
            validated_data.get("origin_ip", instance.origin_ip) != instance.origin_ip
            or validated_data.get("origin_port", instance.origin_port)
            != instance.origin_port
            or validated_data.get("origin_protocol", instance.origin_protocol)
            != instance.origin_protocol
        ):
            # add forward port for new instance
            port = nfportpool.allocate()
            validated_data["forward_port"] = port
        # update
        newinstance = super().update(instance, validated_data)
        if port is not None:
            # remove forwarding controller for old instance
            nfmanager.remove_forwarding_controller(instance.pk)
            # add forwarding controller for new instance
            nfmanager.add_forwarding_controller(
                id=newinstance.pk,
                src_ip=newinstance.origin_ip,
                src_port=newinstance.origin_port,
                src_protocal=to_common_protocol(newinstance.origin_protocol),
                dst_ip=nf_ip_binding,
                dst_port=newinstance.forward_port,
            )
        if newinstance.is_active:
            nfmanager.start_forwarding(newinstance.pk)
        elif port is None:
            nfmanager.stop_forwarding(newinstance.pk)
        return newinstance
