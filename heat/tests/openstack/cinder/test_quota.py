#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import mock

from heat.common import template_format
from heat.engine.clients.os import cinder as c_plugin
from heat.engine import stack as parser
from heat.engine import template
from heat.tests import common
from heat.tests import utils

quota_template = '''
heat_template_version: newton

description: Sample cinder quota heat template

resources:
  my_quota:
    type: OS::Cinder::Quota
    properties:
      project: demo
      gigabytes: 1
      snapshots: 2
      volumes: 3
'''


class CinderQuotaTest(common.HeatTestCase):
    def setUp(self):
        super(CinderQuotaTest, self).setUp()

        self.ctx = utils.dummy_context()
        self.patchobject(c_plugin.CinderClientPlugin, 'has_extension',
                         return_value=True)
        tpl = template_format.parse(quota_template)
        self.stack = parser.Stack(
            self.ctx, 'cinder_quota_test_stack',
            template.Template(tpl)
        )

        self.my_quota = self.stack['my_quota']
        cinder = mock.MagicMock()
        self.cinderclient = mock.MagicMock()
        self.my_quota.client = cinder
        cinder.return_value = self.cinderclient
        self.project_id = '41f0e60c-ebb4-4375-a2b4-845ae8b9c995'
        keystone = mock.MagicMock()
        keystone.get_project_id = mock.MagicMock(return_value=self.project_id)
        self.my_quota.client_plugin = mock.MagicMock(return_value=keystone)
        self.quotas = self.cinderclient.quotas
        self.quota_set = mock.MagicMock()
        self.quotas.update.return_value = self.quota_set
        self.quotas.delete.return_value = self.quota_set

    def test_quota_handle_create(self):
        quota_set = self.my_quota.handle_create()

        self.quotas.update.assert_called_once_with(
            self.project_id,
            gigabytes=1,
            snapshots=2,
            volumes=3
        )
        self.assertEqual(quota_set, self.quota_set)

    def test_quota_handle_update(self):
        json_snippet = mock.MagicMock()
        tmpl_diff = mock.MagicMock()
        prop_diff = {'gigabytes': 2, 'volumes': 4}
        quota_set = self.my_quota.handle_update(
            json_snippet, tmpl_diff, prop_diff)

        self.quotas.update.assert_called_once_with(
            self.project_id,
            gigabytes=2,
            volumes=4
        )
        self.assertEqual(quota_set, self.quota_set)

    def test_quota_handle_delete(self):
        quota_set = self.my_quota.handle_delete()

        self.quotas.delete.assert_called_once_with(self.project_id)
        self.assertEqual(quota_set, self.quota_set)
