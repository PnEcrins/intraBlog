from django.contrib.auth.hashers import make_password
from django.test import TestCase

from django.db import connections
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.test.utils import override_settings
from django.urls import reverse
from django.contrib.auth.models import Group

# from .base import AuthentFixturesMixin
# from ..models import Structure
from ..backend import DatabaseBackend
from .factories import GroupFactory


_CREATE_TABLE_STATEMENT = """
    CREATE TABLE %s (
        username character varying(128) default '',
        first_name character varying(128) default '',
        last_name character varying(128) default '',
        password character varying(128) default '',
        email character varying(128) default ''
    )"""

def query_db(sqlquery):
    connection = connections[settings.AUTHENT_DATABASE or 'default']
    with connection.cursor() as cursor:
        cursor.execute(sqlquery)

@override_settings(AUTHENT_DATABASE='default',
                   AUTHENT_TABLENAME='authent_table',
                   AUTHENTICATION_BACKENDS=('authent.backend.DatabaseBackend',))
class AuthentDatabaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.backend = DatabaseBackend()
        query_db(_CREATE_TABLE_STATEMENT % settings.AUTHENT_TABLENAME)
        cls.deleted = False
        cls.group = GroupFactory()

    @override_settings(AUTHENT_DATABASE=None)
    def test_base_missing(self):
        self.assertRaises(ImproperlyConfigured, self.backend.authenticate, ('toto', 'totopwd'))

    @override_settings(AUTHENT_TABLENAME=None)
    def test_table_missing(self):
        self.assertRaises(ImproperlyConfigured, self.backend.authenticate, ('toto', 'totopwd'))

    @override_settings(AUTHENT_DEFAULT_USER_GROUP_NAME="test")
    def test_login(self):
        query_db("INSERT INTO %s (username, password) VALUES ('joe', '%s')" % (settings.AUTHENT_TABLENAME, make_password('joe')))
        success = self.client.login(username="joe", password="joe")
        self.assertTrue(success)