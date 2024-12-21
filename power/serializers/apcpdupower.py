from common.core.serializers import (
    BaseModelSerializer,
    LabeledChoiceField,
    BasePrimaryKeyRelatedField,
)
from power import models
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.db import transaction
import logging
from power.services import apservice

logger = logging.getLogger(__name__)


class ApcPduPowerUserSerializer(BaseModelSerializer):
    class Meta:
        model = models.ApcPduPower
        # The pk field is used for front-end deletion, update, and other identification purposes. If there is a deletion or update, the pk field must be added
        fields = [
            "pk",
            "id",
            "name",
            "type",
            "ip",
            "port",
            "username",
            "password",
            "description",
            "creator",
            "created_time",
            "updated_time",
        ]
        # Used for displaying table fields in the frontend
        table_fields = [
            "id",
            "name",
            "type",
            "ip",
            "port",
            "username",
            "password",
            "description",
            "creator",
        ]
        read_only_fields = ["pk", "id", "creator"]
        fields_unexport = ["pk"]  # Ignore this field when importing or exporting files

    creator = BasePrimaryKeyRelatedField(
        attrs=["pk", "username"], read_only=True, label=_("Creator")
    )
    type = LabeledChoiceField(
        choices=models.ApcPduPower.OutletTypeChoices.choices,
        label=_("type"),
    )

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            for i in range(1, instance.type + 1):
                models.ApcPduPowerUnit(
                    power=instance,
                    outlet=i,
                    creator=instance.creator,
                    modifier=instance.modifier,
                ).save()
        if instance.is_active:
            apservice.add(
                id=instance.id,
                ip=instance.ip,
                port=instance.port,
                username=instance.username,
                password=instance.password,
            )
        return instance

    def update(self, instance, validated_data):
        old_active = instance.is_active
        old_type = instance.type
        with transaction.atomic():
            newinstance = super().update(instance, validated_data)
            if old_type != newinstance.type:
                if old_type == models.ApcPduPower.OutletTypeChoices.OUTLET_24.value:
                    models.ApcPduPowerUnit.objects.filter(
                        power=instance,
                        outlet__gt=models.ApcPduPower.OutletTypeChoices.OUTLET_8.value,
                    ).delete()
                else:
                    for i in range(
                        models.ApcPduPower.OutletTypeChoices.OUTLET_8.value + 1,
                        newinstance.type + 1,
                    ):
                        models.ApcPduPowerUnit(
                            power=newinstance,
                            outlet=i,
                            creator=newinstance.creator,
                            modifier=newinstance.modifier,
                        ).save()
        if old_active:
            apservice.remove(instance.id)
        if newinstance.is_active:
            apservice.add(
                id=instance.id,
                ip=instance.ip,
                port=instance.port,
                username=instance.username,
                password=instance.password,
            )
        return newinstance


class ApcPduPowerAdminSerializer(ApcPduPowerUserSerializer):
    pass


class ApcPduPowerUnitUserSerializer(BaseModelSerializer):
    class Meta:
        model = models.ApcPduPowerUnit
        # The pk field is used for front-end deletion, update, and other identification purposes. If there is a deletion or update, the pk field must be added
        fields = [
            "pk",
            "id",
            "power",
            "outlet",
            "status",
            "description",
            "creator",
            "created_time",
            "updated_time",
        ]
        # Used for displaying table fields in the frontend
        table_fields = [
            "id",
            "power",
            "outlet",
            "status",
            "description",
            "creator",
        ]
        read_only_fields = ["pk", "id", "creator", "power", "outlet", "status"]
        fields_unexport = ["pk"]  # Ignore this field when importing or exporting files

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["status"] = apservice.power_status(
            instance.power.id, instance.outlet, True
        )[0]
        return rep

    power = BasePrimaryKeyRelatedField(
        attrs=["pk", "name", "type", "ip", "port"],
        read_only=True,
        label=_("PowerController"),
    )
    creator = BasePrimaryKeyRelatedField(
        attrs=["pk", "username"], read_only=True, label=_("Creator")
    )
