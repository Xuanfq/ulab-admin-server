from common.core.serializers import (
    BaseModelSerializer,
    LabeledChoiceField,
    BasePrimaryKeyRelatedField,
)
from nettraversal import models
from django.utils.translation import gettext as _
from rest_framework import serializers
from nettraversal.service.netforward import nfmanager, nfportpool, nf_ip_binding
import logging

logger = logging.getLogger(__name__)


def to_common_protocol(protocol):
    if protocol in ["TCP", "SSH", "RDP", "HTTP", "HTTPS", "TELNET"]:
        return "TCP"
    elif protocol == models.NetForward.ProtocolChoices.UDP:
        return "UDP"
    else:
        return "TCP"


class NetForwardUserSerializer(BaseModelSerializer):
    class Meta:
        model = models.NetForward
        # The pk field is used for front-end deletion, update, and other identification purposes. If there is a deletion or update, the pk field must be added
        fields = [
            "pk",
            "creator",
            "src_ip",
            "src_port",
            "protocol",
            "dst_ip",
            "dst_port",
            "is_active",
            "created_time",
            "updated_time",
            "description",
        ]
        # Used for displaying table fields in the frontend
        table_fields = [
            "pk",
            "creator",
            "src_ip",
            "src_port",
            "protocol",
            "dst_ip",
            "dst_port",
            "is_active",
            "description",
        ]
        read_only_fields = ["pk", "src_ip", "src_port"]
        fields_unexport = ["pk"]  # Ignore this field when importing or exporting files

    creator = BasePrimaryKeyRelatedField(
        attrs=["pk", "username"], read_only=True, label=_("创建者")
    )
    protocol = LabeledChoiceField(
        choices=models.NetForward.ProtocolChoices.choices,
        label=_("协议类型"),
    )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["src_ip"] = nf_ip_binding
        return rep

    def create(self, validated_data):
        # add forward port
        port = nfportpool.allocate()
        validated_data["dst_port"] = port
        # create
        instance = super().create(validated_data)
        # add forwarding controller
        nfmanager.add_forwarding_controller(
            id=instance.pk,
            src_ip=nf_ip_binding,
            src_port=instance.src_port,
            protocol=to_common_protocol(instance.protocol),
            dst_ip=instance.dst_ip,
            dst_port=instance.dst_port,
        )
        if instance.is_active:
            nfmanager.start_forwarding(instance.pk)
            
        return instance

    def update(self, instance, validated_data):
        port = None
        if (
            validated_data.get("dst_ip", instance.dst_ip) != instance.dst_ip
            or validated_data.get("dst_port", instance.dst_port)
            != instance.dst_port
            or validated_data.get("protocol", instance.protocol)
            != instance.protocol
        ):
            # add forward port for new instance
            port = nfportpool.allocate()
            validated_data["src_port"] = port
        # update
        newinstance = super().update(instance, validated_data)
        if port is not None or nfmanager.get_forwarding_controller(instance.pk) is None:
            # remove forwarding controller for old instance
            nfmanager.remove_forwarding_controller(instance.pk)
            # add forwarding controller for new instance
            nfmanager.add_forwarding_controller(
                id=newinstance.pk,
                src_ip=nf_ip_binding,
                src_port=newinstance.src_port,
                protocol=to_common_protocol(newinstance.protocol),
                dst_ip=newinstance.dst_port,
                dst_port=newinstance.dst_port,
            )
        if newinstance.is_active:
            nfmanager.start_forwarding(newinstance.pk)
        elif port is None:
            nfmanager.stop_forwarding(newinstance.pk)
        return newinstance


class NetForwardAdminSerializer(NetForwardUserSerializer):
    pass
