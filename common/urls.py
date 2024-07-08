from django.urls import re_path

from common.api.common import ResourcesIDCacheApi

urlpatterns = [
    re_path('^resources/cache$', ResourcesIDCacheApi.as_view(), name='resources-cache'),
]
