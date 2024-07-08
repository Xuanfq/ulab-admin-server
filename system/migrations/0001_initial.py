# Generated by Django 5.0.6 on 2024-07-08 14:32

import common.core.models
import common.fields.image
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('mode_type', models.SmallIntegerField(choices=[(0, 'OR Mode'), (1, 'AND Mode')], default=0, verbose_name='Data Permission Mode')),
                ('avatar', common.fields.image.ProcessedImageField(blank=True, null=True, upload_to=common.core.models.upload_directory_path, verbose_name='User Avatar')),
                ('nickname', models.CharField(blank=True, max_length=150, verbose_name='Nickname')),
                ('gender', models.IntegerField(choices=[(0, 'Confidential'), (1, 'Male'), (2, 'Female')], default=0, verbose_name='Gender')),
                ('mobile', models.CharField(blank=True, default='', max_length=16, verbose_name='Mobile Number')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User Information',
                'verbose_name_plural': 'User Information',
                'ordering': ('-date_joined',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DataPermission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Primary Key ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('mode_type', models.SmallIntegerField(choices=[(0, 'OR Mode'), (1, 'AND Mode')], default=0, verbose_name='Data Permission Mode')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Data Permission Name')),
                ('rules', models.JSONField(default=list, max_length=512, verbose_name='Rules')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Enabled')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
            ],
            options={
                'verbose_name': 'Data Permission',
                'verbose_name_plural': 'Data Permission',
            },
        ),
        migrations.AddField(
            model_name='userinfo',
            name='rules',
            field=models.ManyToManyField(blank=True, null=True, to='system.datapermission', verbose_name='Data Permission'),
        ),
        migrations.CreateModel(
            name='DeptInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Primary Key ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('mode_type', models.SmallIntegerField(choices=[(0, 'OR Mode'), (1, 'AND Mode')], default=0, verbose_name='Data Permission Mode')),
                ('name', models.CharField(max_length=128, verbose_name='Department Name')),
                ('code', models.CharField(max_length=128, unique=True, verbose_name='Department Identifier')),
                ('rank', models.IntegerField(default=99, verbose_name='Order')),
                ('auto_bind', models.BooleanField(default=False, verbose_name='Is Department Bound')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Enabled')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='parent_query', to='system.deptinfo', verbose_name='Parent Department')),
                ('rules', models.ManyToManyField(blank=True, null=True, to='system.datapermission', verbose_name='Data Permission')),
            ],
            options={
                'verbose_name': 'Department Information',
                'verbose_name_plural': 'Department Information',
                'ordering': ('-rank', '-created_time'),
            },
        ),
        migrations.AddField(
            model_name='datapermission',
            name='dept_belong',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_query_name='dept_query', to='system.deptinfo', verbose_name='Department'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='dept_belong',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department'),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Primary Key ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('menu_type', models.SmallIntegerField(choices=[(0, 'Directory'), (1, 'Menu'), (2, 'Permission')], default=0, verbose_name='Node Type')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Component English Name or Permission Identifier')),
                ('rank', models.IntegerField(default=9999, verbose_name='Menu Order')),
                ('path', models.CharField(max_length=255, verbose_name='Route Address/Backend Permission Route')),
                ('component', models.CharField(blank=True, max_length=255, null=True, verbose_name='Component Address')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Menu Enabled')),
                ('method', models.CharField(blank=True, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('PATCH', 'PATCH')], max_length=10, null=True, verbose_name='Request Method')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.menu', verbose_name='Parent Node')),
            ],
            options={
                'verbose_name': 'Menu Information',
                'verbose_name_plural': 'Menu Information',
                'ordering': ('-created_time',),
            },
        ),
        migrations.AddField(
            model_name='datapermission',
            name='menu',
            field=models.ManyToManyField(blank=True, null=True, to='system.menu', verbose_name='Permission Menu'),
        ),
        migrations.CreateModel(
            name='MenuMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Primary Key ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Menu Name')),
                ('icon', models.CharField(blank=True, max_length=255, null=True, verbose_name='Menu Icon')),
                ('r_svg_name', models.CharField(blank=True, help_text='Additional icon iconfont name on the right side of the menu, currently only iconfont is supported', max_length=255, null=True, verbose_name='Menu Extra Icon')),
                ('is_show_menu', models.BooleanField(default=True, verbose_name='Is Menu Visible')),
                ('is_show_parent', models.BooleanField(default=False, verbose_name='Is Parent Menu Visible')),
                ('is_keepalive', models.BooleanField(default=False, help_text='When enabled, the entire state of the page will be saved, and the state will be cleared after refreshing', verbose_name='Is Page Caching Enabled')),
                ('frame_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Embedded Iframe Link Address')),
                ('frame_loading', models.BooleanField(default=False, verbose_name='Is First Load Animation Enabled for Embedded Iframe Page')),
                ('transition_enter', models.CharField(blank=True, max_length=255, null=True, verbose_name='Current Page Entry Animation')),
                ('transition_leave', models.CharField(blank=True, max_length=255, null=True, verbose_name='Current Page Exit Animation')),
                ('is_hidden_tag', models.BooleanField(default=False, verbose_name='Current Menu Name or Custom Information is Prohibited from Adding to Tab Page')),
                ('fixed_tag', models.BooleanField(default=False, verbose_name='Is Current Menu Name Fixed Displayed in Tab Page and Cannot Be Closed')),
                ('dynamic_level', models.IntegerField(default=1, verbose_name='Maximum Number of Displayed Tab Pages')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
            ],
            options={
                'verbose_name': 'Menu Unit Data',
                'verbose_name_plural': 'Menu Unit Data',
                'ordering': ('-created_time',),
            },
        ),
        migrations.AddField(
            model_name='menu',
            name='meta',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='system.menumeta', verbose_name='Menu Unit Data'),
        ),
        migrations.CreateModel(
            name='ModelLabelField',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Primary Key ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('field_type', models.SmallIntegerField(choices=[(0, 'Role Permission'), (1, 'Data Permission')], default=1, verbose_name='Field Type')),
                ('name', models.CharField(max_length=128, verbose_name='Model/Field Value')),
                ('label', models.CharField(max_length=128, verbose_name='Model/Field Name')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.modellabelfield', verbose_name='Parent Node')),
            ],
            options={
                'verbose_name': 'Model Field',
                'verbose_name_plural': 'Model Field',
                'unique_together': {('name', 'parent')},
            },
        ),
        migrations.AddField(
            model_name='menu',
            name='model',
            field=models.ManyToManyField(blank=True, null=True, to='system.modellabelfield', verbose_name='Bound Model'),
        ),
        migrations.CreateModel(
            name='NoticeMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('level', models.CharField(choices=[('info', 'General Notification'), ('primary', 'General Notification'), ('success', 'Success Notification'), ('danger', 'Important Notification')], default='info', max_length=20, verbose_name='Message Level')),
                ('notice_type', models.SmallIntegerField(choices=[(0, 'System Notification'), (1, 'System Announcement'), (2, 'User Notification'), (3, 'Department Notification'), (4, 'Role Notification')], default=2, verbose_name='Message Type')),
                ('title', models.CharField(max_length=255, verbose_name='Message Title')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Specific Information Content')),
                ('extra_json', models.JSONField(blank=True, null=True, verbose_name='Additional JSON Data')),
                ('publish', models.BooleanField(default=True, verbose_name='Is Published')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
                ('notice_dept', models.ManyToManyField(blank=True, null=True, to='system.deptinfo', verbose_name='Notified Department')),
            ],
            options={
                'verbose_name': 'Message Notification',
                'verbose_name_plural': 'Message Notification',
                'ordering': ('-created_time',),
            },
        ),
        migrations.CreateModel(
            name='NoticeUserRead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('unread', models.BooleanField(db_index=True, default=True, verbose_name='Is Unread')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
                ('notice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.noticemessage', verbose_name='Message Announcement')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Read Messages',
                'verbose_name_plural': 'User Read Messages',
                'ordering': ('-created_time',),
                'unique_together': {('owner', 'notice')},
                'index_together': {('owner', 'unread')},
            },
        ),
        migrations.AddField(
            model_name='noticemessage',
            name='notice_user',
            field=models.ManyToManyField(blank=True, null=True, through='system.NoticeUserRead', to=settings.AUTH_USER_MODEL, verbose_name='Notified User'),
        ),
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('module', models.CharField(blank=True, max_length=64, null=True, verbose_name='Request Module')),
                ('path', models.CharField(blank=True, max_length=400, null=True, verbose_name='Request Address')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Request Parameters')),
                ('method', models.CharField(blank=True, max_length=8, null=True, verbose_name='Request Method')),
                ('ipaddress', models.GenericIPAddressField(blank=True, null=True, verbose_name='Request IP Address')),
                ('browser', models.CharField(blank=True, max_length=64, null=True, verbose_name='Request Browser')),
                ('system', models.CharField(blank=True, max_length=64, null=True, verbose_name='Request Operating System')),
                ('response_code', models.IntegerField(blank=True, null=True, verbose_name='Response Status Code')),
                ('response_result', models.TextField(blank=True, null=True, verbose_name='Response Data')),
                ('status_code', models.IntegerField(blank=True, null=True, verbose_name='Request Status Code')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
            ],
            options={
                'verbose_name': 'Operation Log',
                'verbose_name_plural': 'Operation Log',
                'ordering': ('-created_time',),
            },
        ),
        migrations.CreateModel(
            name='SystemConfig',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Primary Key ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('value', models.TextField(max_length=10240, verbose_name='Configuration Value')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Configuration Item Enabled')),
                ('access', models.BooleanField(default=False, verbose_name='Allow API Access to Configuration')),
                ('key', models.CharField(max_length=255, unique=True, verbose_name='Configuration Name')),
                ('inherit', models.BooleanField(default=False, verbose_name='Allow Users to Inherit Configuration')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
            ],
            options={
                'verbose_name': 'System Configuration Item',
                'verbose_name_plural': 'System Configuration Item',
            },
        ),
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('filepath', models.FileField(blank=True, null=True, upload_to=common.core.models.upload_directory_path, verbose_name='File Storage')),
                ('filename', models.CharField(max_length=150, verbose_name='Original File Name')),
                ('filesize', models.IntegerField(verbose_name='File Size')),
                ('is_tmp', models.BooleanField(default=True, verbose_name='Is Temporary File')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
            ],
            options={
                'verbose_name': 'Uploaded File',
                'verbose_name_plural': 'Uploaded File',
            },
        ),
        migrations.AddField(
            model_name='noticemessage',
            name='file',
            field=models.ManyToManyField(to='system.uploadfile', verbose_name='Uploaded Resource'),
        ),
        migrations.CreateModel(
            name='UserLoginLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('status', models.BooleanField(default=True, verbose_name='Is Login Successful')),
                ('ipaddress', models.GenericIPAddressField(blank=True, null=True, verbose_name='Login IP Address')),
                ('browser', models.CharField(blank=True, max_length=64, null=True, verbose_name='Login Browser')),
                ('system', models.CharField(blank=True, max_length=64, null=True, verbose_name='Operating System')),
                ('agent', models.CharField(blank=True, max_length=128, null=True, verbose_name='Agent Information')),
                ('login_type', models.SmallIntegerField(choices=[(0, 'Password Login'), (1, 'SMS Verification Login'), (2, 'WeChat QR Code Login')], default=0, verbose_name='Login Type')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
            ],
            options={
                'verbose_name': 'Login Log',
                'verbose_name_plural': 'Login Log',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Primary Key ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Role Name')),
                ('code', models.CharField(max_length=128, unique=True, verbose_name='Role Identifier')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Enabled')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('menu', models.ManyToManyField(blank=True, null=True, to='system.menu', verbose_name='Menu Permission')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
            ],
            options={
                'verbose_name': 'Role Information',
                'verbose_name_plural': 'Role Information',
                'ordering': ('-created_time',),
            },
        ),
        migrations.AddField(
            model_name='noticemessage',
            name='notice_role',
            field=models.ManyToManyField(blank=True, null=True, to='system.userrole', verbose_name='Notified Role'),
        ),
        migrations.AddField(
            model_name='deptinfo',
            name='roles',
            field=models.ManyToManyField(blank=True, null=True, to='system.userrole', verbose_name='Role'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='roles',
            field=models.ManyToManyField(blank=True, null=True, to='system.userrole', verbose_name='Role'),
        ),
        migrations.CreateModel(
            name='UserPersonalConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('value', models.TextField(max_length=10240, verbose_name='Configuration Value')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Configuration Item Enabled')),
                ('access', models.BooleanField(default=False, verbose_name='Allow API Access to Configuration')),
                ('key', models.CharField(max_length=255, verbose_name='Configuration Name')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name': 'Personal Configuration Item',
                'verbose_name_plural': 'Personal Configuration Item',
                'unique_together': {('owner', 'key')},
            },
        ),
        migrations.CreateModel(
            name='FieldPermission',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='Primary Key ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Add Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('dept_belong', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='dept_belong_query', to='system.deptinfo', verbose_name='Data Department')),
                ('modifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='modifier_query', to=settings.AUTH_USER_MODEL, verbose_name='Modifier')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.menu', verbose_name='Menu')),
                ('field', models.ManyToManyField(blank=True, null=True, to='system.modellabelfield', verbose_name='Field')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.userrole', verbose_name='Role')),
            ],
            options={
                'verbose_name': 'Field Permission Table',
                'verbose_name_plural': 'Field Permission Table',
                'ordering': ('-created_time',),
                'unique_together': {('role', 'menu')},
            },
        ),
    ]
