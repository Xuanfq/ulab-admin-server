# Backend Damon

## 1.Create django app

```shell
python3 manage.py startapp demo
```

## 2.Add app to `config.py`

```python
# The created application needs to be written to the file 'config. py', otherwise the model association cannot be found in the menu
ULAB_APPS = [
    'demo.apps.DemoConfig',
]
```

## 3.Edit models

```python
# demo/models.py

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from common.core.models import DbAuditModel, upload_directory_path
from system.models import UserInfo


class Book(DbAuditModel):
    class CategoryChoices(models.IntegerChoices):
        DIRECTORY = 0, _("小说")
        MENU = 1, _("文学")
        PERMISSION = 2, _("哲学")

    # covers = models.ManyToManyField(to=UploadFile,verbose_name="封面")
    admin = models.ForeignKey(to=UserInfo, verbose_name="管理员", on_delete=models.CASCADE)
    # avatar = ProcessedImageField(verbose_name="用户头像", null=True, blank=True,
    #                              upload_to=upload_directory_path,
    #                              processors=[ResizeToFill(512, 512)],  # 默认存储像素大小
    #                              scales=[1, 2, 3, 4],  # 缩略图可缩小倍数，
    #                              format='png')
    cover = models.ImageField(verbose_name="书籍封面", null=True, blank=True)
    book_file = models.FileField(verbose_name="书籍存储", upload_to=upload_directory_path, null=True, blank=True)
    name = models.CharField(verbose_name="书籍名称", max_length=100, help_text="书籍名称啊，随便填")
    isbn = models.CharField(verbose_name="标准书号", max_length=20)
    author = models.CharField(verbose_name="书籍作者", max_length=20, help_text="坐着大啊啊士大夫")
    publisher = models.CharField(verbose_name="出版社", max_length=20, default='大宇出版社')
    publication_date = models.DateTimeField(verbose_name="出版日期", default=timezone.now)
    price = models.FloatField(verbose_name="书籍售价", default=999.99)
    is_active = models.BooleanField(verbose_name="是否启用", default=False)
    category = models.SmallIntegerField(choices=CategoryChoices, default=CategoryChoices.DIRECTORY,
                                        verbose_name="书籍类型")

    class Meta:
        verbose_name = '书籍名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
```

## 4.Edit serializer

### In the 'demo' directory, create a new 'utilities' directory, and then create the' serializer. py 'file in the' utilities' directory

```python
# demo/utils/serializer.py

from common.core.serializers import BaseModelSerializer, LabeledChoiceField, BasePrimaryKeyRelatedField
from demo import models


class BookSerializer(BaseModelSerializer):
    class Meta:
        model = models.Book
        ## The pk field is used for front-end deletion, update, and other identification purposes. If there is a deletion or update, the pk field must be added
        fields = ['pk', 'name', 'isbn', 'category', 'is_active', 'author', 'publisher', 'publication_date', 'price',
                  'created_time', 'admin', 'cover', 'book_file', 'updated_time']
        ## Used for displaying table fields in the frontend
        table_fields = ['pk', 'cover', 'category', 'name', 'is_active', 'isbn', 'author', 'publisher',
                        'publication_date', 'price', 'book_file']
        read_only_fields = ['pk']
        # fields_unexport = ['pk']  # Ignore this field when importing or exporting files

    category = LabeledChoiceField(choices=models.Book.CategoryChoices.choices,
                                  default=models.Book.CategoryChoices.DIRECTORY, label='书籍类型')
    admin = BasePrimaryKeyRelatedField(attrs=['pk', 'username'], label="管理员", queryset=models.UserInfo.objects,
                                       required=True, format="{username}({pk})")
    # covers = BasePrimaryKeyRelatedField(attrs=['pk', 'filename'],format="{filename}({pk})", label="书籍封面", queryset=models.UploadFile.objects,
    #                                    required=True,  many=True)
```

## 5.Edit views

```python
# demo/views.py

# Create your views here.

import logging

from django_filters import rest_framework as filters

from common.core.filter import BaseFilterSet
from common.core.modelset import BaseModelSet, ImportExportDataAction
from demo.models import Book
from demo.utils.serializer import BookSerializer

logger = logging.getLogger(__name__)


class BookFilter(BaseFilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author', lookup_expr='icontains')
    publisher = filters.CharFilter(field_name='publisher', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['name', 'isbn', 'author', 'publisher', 'is_active', 'publication_date', 'price',
                  'created_time']  # Fields are used for front-end automatic generation of search forms


class BookView(BaseModelSet, ImportExportDataAction):
    """
    书籍管理
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    ordering_fields = ['created_time']
    filterset_class = BookFilter
```

## 6.Create a new 'urls. py' routing file and add a route

```python
# demo/urls.py

from rest_framework.routers import SimpleRouter

from demo.views import BookView

router = SimpleRouter(False)  # Set to False to remove the slash after the URL

router.register('book', BookView, basename='book')

urlpatterns = [
]
urlpatterns += router.urls
```

## 7.Create a new 'config. py' file and add relevant configurations

```python
# demo/config.py
from django.urls import path, include

# Routing configuration, when the APP is added, it will automatically inject routing to the overall service
URLPATTERNS = [
    path('api/demo/', include('demo.urls')),
]

# Request whitelist, supports regular expressions, can refer to PERMission-WeihITE-URL in settings. py
PERMISSION_WHITE_REURL = [
    "^/api/demo/.*choices$",
    "^/api/demo/.*search-fields$",
]
```

## 8.Migration demo application

```python
python manage.py makemigrations
python manage.py migrate
```
