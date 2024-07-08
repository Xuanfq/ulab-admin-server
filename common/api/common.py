import uuid

from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from common.cache.storage import CommonResourceIDsCache
from common.core.response import ApiResponse


class ResourcesIDCacheApi(APIView):
    """
    资源ID缓存
    Resource ID Cache
    """
    permission_classes = []

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['resources'],
        properties={'resources': openapi.Schema(description = _("主键列表"), type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(type=openapi.TYPE_STRING))}
    ), operation_description = _("将资源数据临时保存到服务器"))
    def post(self, request, *args, **kwargs):
        spm = str(uuid.uuid4())
        resources = request.data.get('resources')
        if resources is not None:
            CommonResourceIDsCache(spm).set_storage_cache(resources, 300)
        return ApiResponse(spm=spm)
