# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from sqlalchemy import and_
from sqlalchemy import exc
from sqlalchemy import or_

from schematizer.logic.validators import verify_entity_exists
from schematizer.models import AvroSchema
from schematizer.models import MetaAttributeMappingStore
from schematizer.models import Namespace
from schematizer.models import Source
from schematizer.models.database import session


def _register_meta_attribute_for_entity(
    meta_attr_sch_id,
    entity_model,
    entity_id
):
    verify_entity_exists(session, entity_model, entity_id)
    verify_entity_exists(session, AvroSchema, meta_attr_sch_id)
    try:
        with session.begin_nested():
            new_mapping = MetaAttributeMappingStore(
                entity_type=entity_model.__name__,
                entity_id=entity_id,
                meta_attr_schema_id=meta_attr_sch_id
            )
            session.add(new_mapping)
    except exc.IntegrityError:
        # Ignore this error due to trying to create a duplicate mapping
        new_mapping = session.query(
            MetaAttributeMappingStore
        ).filter(
            MetaAttributeMappingStore.entity_type == entity_model.__name__,
            MetaAttributeMappingStore.entity_id == entity_id,
            MetaAttributeMappingStore.meta_attr_schema_id == meta_attr_sch_id
        ).one()
    return new_mapping


def _delete_meta_attribute_mapping_for_entity(
    meta_attr_sch_id,
    entity_model,
    entity_id
):
    verify_entity_exists(session, entity_model, entity_id)
    verify_entity_exists(session, AvroSchema, meta_attr_sch_id)
    return bool(
        session.query(
            MetaAttributeMappingStore
        ).filter(
            MetaAttributeMappingStore.entity_type == entity_model.__name__,
            MetaAttributeMappingStore.entity_id == entity_id,
            MetaAttributeMappingStore.meta_attr_schema_id == meta_attr_sch_id
        ).delete()
    )


def register_namespace_meta_attribute_mapping(
    meta_attr_schema_id,
    namespace_id
):
    return _register_meta_attribute_for_entity(
        meta_attr_sch_id=meta_attr_schema_id,
        entity_model=Namespace,
        entity_id=namespace_id
    )


def register_source_meta_attribute_mapping(
    meta_attr_schema_id,
    source_id
):
    return _register_meta_attribute_for_entity(
        meta_attr_sch_id=meta_attr_schema_id,
        entity_model=Source,
        entity_id=source_id
    )


def register_schema_meta_attribute_mapping(
    meta_attr_schema_id,
    schema_id
):
    return _register_meta_attribute_for_entity(
        meta_attr_sch_id=meta_attr_schema_id,
        entity_model=AvroSchema,
        entity_id=schema_id
    )


def delete_namespace_meta_attribute_mapping(
    meta_attr_schema_id,
    namespace_id
):
    return _delete_meta_attribute_mapping_for_entity(
        meta_attr_sch_id=meta_attr_schema_id,
        entity_model=Namespace,
        entity_id=namespace_id
    )


def delete_source_meta_attribute_mapping(
    meta_attr_schema_id,
    source_id
):
    return _delete_meta_attribute_mapping_for_entity(
        meta_attr_sch_id=meta_attr_schema_id,
        entity_model=Source,
        entity_id=source_id
    )


def delete_schema_meta_attribute_mapping(
    meta_attr_schema_id,
    schema_id
):
    return _delete_meta_attribute_mapping_for_entity(
        meta_attr_sch_id=meta_attr_schema_id,
        entity_model=AvroSchema,
        entity_id=schema_id
    )


def _filter_param_for_namespace(namespace_id):
    return and_(
        MetaAttributeMappingStore.entity_type == Namespace.__name__,
        MetaAttributeMappingStore.entity_id == namespace_id
    )


def _filter_param_for_source(source_id):
    return and_(
        MetaAttributeMappingStore.entity_type == Source.__name__,
        MetaAttributeMappingStore.entity_id == source_id
    )


def _filter_param_for_schema(schema_id):
    return and_(
        MetaAttributeMappingStore.entity_type == AvroSchema.__name__,
        MetaAttributeMappingStore.entity_id == schema_id
    )


def _get_meta_attributes_by_filters(filters):
    qry = session.query(MetaAttributeMappingStore)
    if filters is not None:
        qry = qry.filter(filters)
    results = qry.order_by(MetaAttributeMappingStore.meta_attr_schema_id).all()
    return [m.meta_attr_schema_id for m in results]


def get_meta_attributes_by_namespace(namespace_id):
    """Logic method to list meta attributes registered to a given namespace_id.
    Invalid namespace ids will raise an EntityNotFoundError exception"""
    Namespace.get_by_id(namespace_id)
    return _get_meta_attributes_by_filters(
        _filter_param_for_namespace(namespace_id)
    )


def get_meta_attributes_by_source(source_id):
    """Logic method to list meta attributes registered to a given source_id and
    the namespace it belongs to. Invalid source ids will raise an
    EntityNotFoundError exception"""
    source = Source.get_by_id(source_id)
    return _get_meta_attributes_by_filters(
        or_(
            _filter_param_for_namespace(source.namespace_id),
            _filter_param_for_source(source.id)
        )
    )


def get_meta_attributes_by_schema(avro_schema_id):
    """Logic method to list meta attributes registered to a given schema_id and
    the namespace and source it belongs to. Invalid schema ids will raise an
    EntityNotFoundError exception"""
    avro_schema = AvroSchema.get_by_id(avro_schema_id)
    source_id = avro_schema.topic.source_id
    namespace_id = avro_schema.topic.source.namespace_id
    return _get_meta_attributes_by_filters(
        or_(
            _filter_param_for_namespace(namespace_id),
            _filter_param_for_source(source_id),
            _filter_param_for_schema(avro_schema.id)
        )
    )
