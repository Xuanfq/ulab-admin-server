import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from django.utils.translation import gettext as _

from common.base.magic import cache_response
from common.base.utils import get_choices_dict, AESCipherV2
from common.core.modelset import OwnerModelSet, UploadFileAction
from common.core.response import ApiResponse
from system.models import UserInfo
from system.utils.serializer import UserInfoSerializer

logger = logging.getLogger(__name__)


class UserInfoView(OwnerModelSet, UploadFileAction):
    """
    用户个人信息管理
    User Personal Information Management
    """
    serializer_class = UserInfoSerializer
    FILE_UPLOAD_FIELD = 'avatar'
    choices_models = [UserInfo]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return UserInfo.objects.filter(pk=self.request.user.pk)

    def get_cache_key(self, view_instance, view_method, request, args, kwargs):
        func_name = f'{view_instance.__class__.__name__}_{view_method.__name__}'
        return f"{func_name}_{request.user.pk}"

    @cache_response(timeout=600, key_func='get_cache_key')
    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        return ApiResponse(**data, choices_dict=get_choices_dict(UserInfo.GenderChoices.choices))

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['old_password', 'sure_password'],
        properties={'old_password': openapi.Schema(description = _("旧密码"), type=openapi.TYPE_STRING),
                    'sure_password': openapi.Schema(description = _("新密码"), type=openapi.TYPE_STRING)}
    ), operation_description = _("修改个人密码"))
    @action(methods=['post'], detail=False, url_path='reset-password')
    def reset_password(self, request, *args, **kwargs):
        old_password = request.data.get('old_password')
        sure_password = request.data.get('sure_password')
        if old_password and sure_password:
            instance = self.get_object()
            sure_password = AESCipherV2(instance.username).decrypt(sure_password)
            old_password = AESCipherV2(instance.username).decrypt(old_password)
            if not instance.check_password(old_password):
                return ApiResponse(code=1001, detail = _("旧密码校验失败"))
            instance.set_password(sure_password)
            instance.modifier = request.user
            instance.save(update_fields=['password', 'modifier'])
            return ApiResponse()
        return ApiResponse(code=1001, detail = _("修改失败"))
