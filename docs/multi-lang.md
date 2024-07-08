
# Multi Language Support

## Overview

This project is designed to support multiple languages. If you want to use another language, you can set the language in the following steps.

## Configuration

To set the language, you can use the `language` option in the configuration file. The available languages are:

- `en`: English
- `zh`: Chinese

### Set available languages

You can set the available languages in the `settings.py` or `config.py` file. For example:

```yaml
LANGUAGE_CODE = 'en'
```

### Set other languages or Update available languages

You can set other languages or update the available languages in the `settings.py` or `config.py` file. For example:

- Using translation in code:

```python
from django.utils.translation import gettext as _

print(_('Hello, World!'))
```

- Using translation in templates:

```html
{% load i18n %}
{% get_current_language as LANGUAGE_CODE %}
{% get_current_language_bidi as LANGUAGE_BIDI %}
{% get_language_info for LANGUAGE_CODE as LANGUAGE_INFO %}
{% get_language_info_list for LANGUAGES as LANGUAGES_INFO_LIST %}
{% get_language_info_list for LANGUAGES_BIDI as LANGUAGES_BIDI_INFO_LIST %}
{% get_language_info_list for LANGUAGES_ALL as LANGUAGES_ALL_INFO_LIST %}
{% get_language_info_list for LANGUAGES_ALL_BIDI as LANGUAGES_ALL_BIDI_INFO_LIST %}
```

- After you using translation, pls comfirm that you have added a directory named `locale` in your `app` which uses translation.

- Then you can use the `makemessages` command to generate the translation files:

```bash
# cd BASE_DIR of your project
python manage.py makemessages -l en
# cd BASE_DIR of your project
python manage.py makemessages -l zh
```

- Followings, you should add the translation in the generated files.

For example, you can add the translation in the `app/locale/en_US/LC_MESSAGES/django.po` file:

```po
msgid "Hello, World!"
msgstr "你好，世界！"
```

- Then you should use the `compilemessages` command to compile the translation files:

```bash
# cd BASE_DIR of your project
python manage.py compilemessages
```

## Reference

- [Django Internationalization and Localization](https://docs.djangoproject.com/en/3.2/topics/i18n/)