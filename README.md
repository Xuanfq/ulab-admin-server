# ulab-admin-server
A admin server for ulab.

## How to start

### 1. Environment Setup

#### Environment Dependencies

```text
python >=3.12
nodejs >=20  # for web
redis >=6
mariadb > 10.5 or mysql > 8.0
```

#### Database Support

- PostgreSQL
- MariaDB
- MySQL
- Oracle
- SQLite

Reference：https://docs.djangoproject.com/zh-hans/5.0/ref/databases/

#### Environment Install

base on Ubuntu 20.04

- Python

```shell
sudo apt install -y python3
```

- Mysql

```shell
sudo apt install -y mysql-server libmysqlclient-dev pymysql
```

- Redis

```shell
sudo apt install -y redis-server
```

- Nodejs

...

- requirement

```shell
pip install -r requirements.txt
```

### 2. Start the Project

#### Initialize the Project

```shell
# python manage.py makemessages -l en
# python manage.py makemessages -l zh
python manage.py compilemessages
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py init_data
```

#### Run the Project

```shell
python manage.py start all
```

## Docs

[How to start](./docs/start.md)
[How to deploy](./docs/deploy.md)
[Multi Lang](./docs/multi-lang.md)
[Develop Daemon (Backend Daemon)](./docs/backend%20damon.md)
[Develop Daemon (Frontend)](./docs/web.md)
[App Service Daemon](./docs/app%20service%20daemon.md)
[Data Permission](./docs/data-permission.md)
[Field Permission](./docs/field-permission.md)