# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from pyramid.view import view_config

from schematizer.api.decorators import transform_api_response
from schematizer.api.exceptions import exceptions_v1
from schematizer.api.requests import requests_v1
from schematizer.api.responses import responses_v1
from schematizer.logic import meta_attribute_mappers as meta_attr_logic
from schematizer.models import Namespace
from schematizer.models.exceptions import EntityNotFoundError


def _register_meta_attribute_mapping_for_entity(request, register_func):
    try:
        req = requests_v1.RegisterMetaAttributeRequest(**request.json_body)
        entity_id = req.entity_id
        meta_attr_schema_id = req.meta_attribute_schema_id
        return register_func(meta_attr_schema_id, entity_id)
    except EntityNotFoundError as e:
        raise exceptions_v1.entity_not_found_exception(e.message)


def _delete_meta_attribute_mapping_for_entity(request, delete_func):
    try:
        req = requests_v1.RegisterMetaAttributeRequest(**request.json_body)
        entity_id = req.entity_id
        meta_attr_schema_id = req.meta_attribute_schema_id
        return delete_func(meta_attr_schema_id, entity_id)
    except EntityNotFoundError as e:
        raise exceptions_v1.entity_not_found_exception(e.message)


@view_config(
    route_name='api.v1.register_namepsace_meta_attribute_mapping',
    request_method='POST',
    renderer='json'
)
@transform_api_response()
def register_namepsace_meta_attribute_mapping(request):
    mapping = _register_meta_attribute_mapping_for_entity(
        request,
        meta_attr_logic.register_namespace_meta_attribute_mapping
    )
    return responses_v1.get_meta_attr_mapping_response(
        'namespace_id',
        mapping.entity_id,
        [mapping.meta_attr_schema_id]
    )


@view_config(
    route_name='api.v1.delete_namespace_meta_attribute_mapping',
    request_method='DELETE',
    renderer='json'
)
@transform_api_response()
def delete_namespace_meta_attribute_mapping(request):
    return _delete_meta_attribute_mapping_for_entity(
        request,
        meta_attr_logic.delete_namespace_meta_attribute_mapping
    )


@view_config(
    route_name='api.v1.register_source_meta_attribute_mapping',
    request_method='POST',
    renderer='json'
)
@transform_api_response()
def register_source_meta_attribute_mapping(request):
    mapping = _register_meta_attribute_mapping_for_entity(
        request,
        meta_attr_logic.register_source_meta_attribute_mapping
    )
    return responses_v1.get_meta_attr_mapping_response(
        'source_id',
        mapping.entity_id,
        [mapping.meta_attr_schema_id]
    )


@view_config(
    route_name='api.v1.delete_source_meta_attribute_mapping',
    request_method='DELETE',
    renderer='json'
)
@transform_api_response()
def delete_source_meta_attribute_mapping(request):
    return _delete_meta_attribute_mapping_for_entity(
        request,
        meta_attr_logic.delete_source_meta_attribute_mapping
    )


@view_config(
    route_name='api.v1.register_schema_meta_attribute_mapping',
    request_method='POST',
    renderer='json'
)
@transform_api_response()
def register_schema_meta_attribute_mapping(request):
    mapping = _register_meta_attribute_mapping_for_entity(
        request,
        meta_attr_logic.register_schema_meta_attribute_mapping
    )
    return responses_v1.get_meta_attr_mapping_response(
        'avroschema_id',
        mapping.entity_id,
        [mapping.meta_attr_schema_id]
    )


@view_config(
    route_name='api.v1.delete_schema_meta_attribute_mapping',
    request_method='DELETE',
    renderer='json'
)
@transform_api_response()
def delete_schema_meta_attribute_mapping(request):
    return _delete_meta_attribute_mapping_for_entity(
        request,
        meta_attr_logic.delete_schema_meta_attribute_mapping
    )


@view_config(
    route_name='api.v1.get_meta_attr_mappings_by_namespace',
    request_method='GET',
)
@transform_api_response()
def get_meta_attr_mappings_by_namespace(request):
    try:
        namespace_name = str(request.matchdict.get('namespace'))
        namespace = Namespace.get_by_name(namespace_name)
        meta_attr_ids = meta_attr_logic.get_meta_attributes_by_namespace(
            namespace.id
        )
        return responses_v1.get_meta_attr_mapping_response(
            'namespace_id', namespace.id, meta_attr_ids
        )
    except EntityNotFoundError as e:
        raise exceptions_v1.entity_not_found_exception(e.message)


@view_config(
    route_name='api.v1.get_meta_attr_mappings_by_source_id',
    request_method='GET',
    renderer='json'
)
@transform_api_response()
def get_meta_attr_mappings_by_source_id(request):
    try:
        source_id = int(request.matchdict.get('source_id'))
        meta_attr_ids = meta_attr_logic.get_meta_attributes_by_source(
            source_id
        )
        return responses_v1.get_meta_attr_mapping_response(
            'source_id', source_id, meta_attr_ids
        )
    except EntityNotFoundError as e:
        raise exceptions_v1.entity_not_found_exception(e.message)


@view_config(
    route_name='api.v1.get_meta_attr_mappings_by_schema_id',
    request_method='GET',
    renderer='json'
)
@transform_api_response()
def get_meta_attr_mappings_by_schema_id(request):
    try:
        schema_id = int(request.matchdict.get('schema_id'))
        meta_attr_ids = meta_attr_logic.get_meta_attributes_by_schema(
            schema_id
        )
        return responses_v1.get_meta_attr_mapping_response(
            'avroschema_id', schema_id, meta_attr_ids
        )
    except EntityNotFoundError as e:
        raise exceptions_v1.entity_not_found_exception(e.message)
