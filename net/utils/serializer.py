from common.core.serializers import (
    BaseModelSerializer,
    LabeledChoiceField,
    BasePrimaryKeyRelatedField,
)
from net import models
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.db import transaction
from net.services import pfservice, pfip, pfportpool
import logging

logger = logging.getLogger(__name__)


def to_common_protocol(protocol):
    if protocol in ["TCP", "SSH", "RDP", "HTTP", "HTTPS", "TELNET"]:
        return "TCP"
    elif protocol == models.PortForward.ProtocolChoices.UDP:
        return "UDP"
    else:
        return "TCP"


class PortForwardUserSerializer(BaseModelSerializer):
    class Meta:
        model = models.PortForward
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
        choices=models.PortForward.ProtocolChoices.choices,
        label=_("协议类型"),
    )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["src_ip"] = pfip
        return rep

    def create(self, validated_data):
        # add forward port
        port = pfportpool.allocate()
        validated_data["src_port"] = port
        # create
        instance = super().create(validated_data)
        if instance.is_active:
            # add forwarding controller
            pfservice.add(
                id=instance.pk,
                src_ip=pfip,
                src_port=instance.src_port,
                protocol=to_common_protocol(instance.protocol),
                dst_ip=instance.dst_ip,
                dst_port=instance.dst_port,
            )

        return instance

    def update(self, instance, validated_data):
        port = None
        if (
            validated_data.get("dst_ip", instance.dst_ip) != instance.dst_ip
            or validated_data.get("dst_port", instance.dst_port) != instance.dst_port
            or to_common_protocol(validated_data.get("protocol", instance.protocol))
            != to_common_protocol(instance.protocol)
        ):
            # add forward port for new instance
            port = pfportpool.allocate()
            validated_data["src_port"] = port
        old_active = instance.is_active
        # update
        newinstance = super().update(instance, validated_data)
        if old_active:
            # remove forwarding for old instance
            pfservice.remove(instance.pk)
        if newinstance.is_active:
            # add forwarding for new instance
            pfservice.add(
                id=newinstance.pk,
                src_ip=pfip,
                src_port=newinstance.src_port,
                protocol=to_common_protocol(newinstance.protocol),
                dst_ip=newinstance.dst_ip,
                dst_port=newinstance.dst_port,
            )
        return newinstance


class PortForwardAdminSerializer(PortForwardUserSerializer):
    pass
