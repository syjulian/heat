.. -*- rst -*-

===============
Stack resources
===============


Find stack resources
====================

.. rest_method::  GET /v1/{tenant_id}/stacks/{stack_name}/resources

Finds the canonical URL for a resource list of a stack.

The canonical URL is returned for only non-deleted stacks. To fetch
the resource list for deleted stacks, use the following endpoint:

::

   /v1/{tenant_id}/stacks/{stack_name}/{stack_id}/resources

Error response codes:302,

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - tenant_id: tenant_id
   - stack_name: stack_name_url


List stack resources
====================

.. rest_method::  GET /v1/{tenant_id}/stacks/{stack_name}/{stack_id}/resources

Lists resources in a stack based on filtering parameters like resource
name, status, type, action, id and physical_resource_id. These parameters could
be used multiple times.

Normal response codes: 200
Error response codes:404,401,400,

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - tenant_id: tenant_id
   - stack_name: stack_name_url
   - stack_id: stack_id_url
   - nested_depth: nested_depth
   - with_detail: with_detail
   - name: resource_name_query
   - status: resource_status
   - type: resource_type
   - action: resource_action
   - id: logical_resource_id
   - physical_resource_id: physical_resource_id

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - resource_name: resource_name
   - description: description
   - logical_resource_id: logical_resource_id
   - creation_time: creation_time
   - resource_status: resource_status
   - updated_time: updated_time
   - required_by: required_by
   - resources: resources
   - resource_status_reason: resource_status_reason
   - physical_resource_id: physical_resource_id
   - resource_type: resource_type

Response Example
----------------

.. literalinclude:: samples/resources-list-response.json
   :language: javascript


Show resource metadata
======================

.. rest_method::  GET /v1/{tenant_id}/stacks/{stack_name}/{stack_id}/resources/{resource_name}/metadata

Shows metadata for a resource.


Normal response codes: 200
Error response codes:

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - tenant_id: tenant_id
   - stack_name: stack_name_url
   - stack_id: stack_id_url
   - resource_name: resource_name_url

Response Example
----------------

.. literalinclude:: samples/resource-metadata-response.json
   :language: javascript


Show resource data
==================

.. rest_method::  GET /v1/{tenant_id}/stacks/{stack_name}/{stack_id}/resources/{resource_name}

Shows data for a resource.


Normal response codes: 200
Error response codes:404,401,400,

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - tenant_id: tenant_id
   - stack_name: stack_name_url
   - stack_id: stack_id_url
   - resource_name: resource_name_url

Response Parameters
-------------------

.. rest_parameters:: parameters.yaml

   - resource_name: resource_name
   - resource: resource
   - description: description
   - logical_resource_id: logical_resource_id
   - creation_time: creation_time
   - resource_status: resource_status
   - updated_time: updated_time
   - required_by: required_by
   - resource_status_reason: resource_status_reason
   - physical_resource_id: physical_resource_id
   - resource_type: resource_type

Response Example
----------------

.. literalinclude:: samples/resource-show-response.json
   :language: javascript


Send a signal to a resource
===========================

.. rest_method::  POST /v1/{tenant_id}/stacks/{stack_name}/{stack_id}/resources/{resource_name}/signal

Sends a signal to a resource.

The contents of the request body depends on the resource to which
you send a signal.

Some resources cannot receive signals. If you send them a signal,
they return a 400 error code.


Normal response codes: 200
Error response codes:

Request Parameters
------------------

.. rest_parameters:: parameters.yaml

   - tenant_id: tenant_id
   - stack_name: stack_name_url
   - stack_id: stack_id_url
   - resource_name: resource_name_url

Response Example
----------------

This operation does not return a response body.
