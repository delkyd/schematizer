# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from schematizer.models.database import Base
from schematizer.models.types.time import build_time_column


class ConsumerGroup(Base):

    __tablename__ = 'consumer_group'
    id = Column(Integer, primary_key=True)
    group_name = Column(String, nullable=False, unique=True)
    data_target_id = Column(
        Integer,
        ForeignKey('data_target.id'),
        nullable=False
    )

    # Timestamp when the entry is created
    created_at = build_time_column(default_now=True, nullable=False)

    # Timestamp when the entry is last updated
    updated_at = build_time_column(
        default_now=True,
        onupdate_now=True,
        nullable=False
    )
