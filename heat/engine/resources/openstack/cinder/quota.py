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

from heat.common.i18n import _
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine import support


class CinderQuota(resource.Resource):
    """A resource for creating cinder quotas.

    Note that default cinder security policy usage of this resource
    is limited to being used by administrators only.
    """

    support_status = support.SupportStatus(version='newton')

    default_client_name = 'cinder'

    entity = 'quotas'

    required_service_extension = 'os-quota-sets'

    PROPERTIES = (PROJECT, GIGABYTES, VOLUMES, SNAPSHOTS) = (
        'project', 'gigabytes', 'volumes', 'snapshots')

    properties_schema = {
        PROJECT: properties.Schema(
            properties.Schema.STRING,
            _('OpenStack Keystone Project'),
            required=True,
            update_allowed=True,
        ),
        GIGABYTES: properties.Schema(
            properties.Schema.INTEGER,
            _('Quota for the amount of disk space (in Gigabytes).'
              'Minimum value is 1.'),
            constraints=[
                constraints.Range(min=1),
            ],
            update_allowed=True
        ),
        VOLUMES: properties.Schema(
            properties.Schema.INTEGER,
            _('Quota for the number of volumes.'
              'Minimum value is 1.'),
            constraints=[
                constraints.Range(min=1),
            ],
            update_allowed=True
        ),
        SNAPSHOTS: properties.Schema(
            properties.Schema.INTEGER,
            _('Quota for the number of snapshots.'
              'Minimum value is 1.'),
            constraints=[
                constraints.Range(min=1),
            ],
            update_allowed=True
        )
    }

    def handle_create(self):
        create_args = {}
        gigabytes = self.properties.get(self.GIGABYTES, None)
        snapshots = self.properties.get(self.SNAPSHOTS, None)
        volumes = self.properties.get(self.VOLUMES, None)

        if gigabytes:
            create_args['gigabytes'] = gigabytes
        if snapshots:
            create_args['snapshots'] = snapshots
        if volumes:
            create_args['volumes'] = volumes

        project = self.properties[self.PROJECT]

        quota_set_manager = self.client().quotas.update(
            self.client_plugin('keystone').get_project_id(project),
            **create_args)

        return quota_set_manager

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        update_args = {}
        gigabytes = prop_diff.get(self.GIGABYTES, None)
        snapshots = prop_diff.get(self.SNAPSHOTS, None)
        volumes = prop_diff.get(self.VOLUMES, None)

        if gigabytes:
            update_args['gigabytes'] = gigabytes
        if snapshots:
            update_args['snapshots'] = snapshots
        if volumes:
            update_args['volumes'] = volumes

        project = self.properties[self.PROJECT]

        quota_set_manager = self.client().quotas.update(
            self.client_plugin('keystone').get_project_id(project),
            **update_args)

        return quota_set_manager

    def handle_delete(self):
        project = self.properties[self.PROJECT]
        quota_set_manager = self.client().quotas.delete(
            self.client_plugin('keystone').get_project_id(project))

        return quota_set_manager


def resource_mapping():
    return {
        'OS::Cinder::Quota': CinderQuota
    }
