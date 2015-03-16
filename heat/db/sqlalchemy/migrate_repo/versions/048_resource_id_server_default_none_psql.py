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

import sqlalchemy


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine
    meta.reflect(meta.bind)

    if migrate_engine.name == 'postgresql':
        resource = sqlalchemy.Table('resource', meta)
        resource.c.id.alter(server_default=None)


def downgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    if migrate_engine.name == 'postgresql':
        resource = sqlalchemy.Table('resource', meta, autoload=True)
        resource.c.id.alter(
            server_default=sqlalchemy.Sequence('resource_id_seq').next_value())