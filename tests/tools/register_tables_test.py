# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from argparse import Namespace
from glob import glob

import mock
import pytest

from schematizer.tools.register_tables import run
from tests.models.testing_db import DBTestCase


class TestRegisterTables(DBTestCase):

    @property
    def schematizer_cluster(self):
        return 'schematizer'

    @pytest.fixture
    def simple_topology_file(self, tmpdir):
        mysql_url = self.engine.url
        local = tmpdir.mkdir("dummy").join("dummy_topology.yaml")
        local.write('''
            topology:
            - cluster: {cluster}
              replica: 'slave'
              entries:
                - charset: utf8
                  host: '{host}'
                  db: '{db}'
                  user: '{user}'
                  passwd: '{passwd}'
                  port: {port}
                  use_unicode: true
        '''.format(
            cluster=self.schematizer_cluster,
            host=mysql_url.host or 'localhost',
            db=mysql_url.database,
            user=mysql_url.username or '',
            port=int(mysql_url.port) or 3306,
            passwd=mysql_url.password or ''
        ))
        return local.strpath

    def test_register_all_schematizer_tables(self, simple_topology_file):
        parsed_args = Namespace(
            cluster_name=self.schematizer_cluster,
            config_file=simple_topology_file
        )
        with mock.patch(
            'schematizer.tools.register_tables.print'
        ) as mock_print:
            run(parsed_args)

            table_count = len(glob('schema/tables/*.sql'))
            expected_call_args_list = [
                mock.call('Registered total {} tables.'.format(table_count)),
                mock.call(
                    '{} tables successfully registered.'.format(table_count)
                ),
                mock.call('0 table failed.')
            ]
            assert mock_print.call_args_list == expected_call_args_list
