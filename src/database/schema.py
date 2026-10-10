"""
Database schema for SQLite.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class Service(Base):
    """Represents a service in the system."""

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(String(50), nullable=False, default="unknown")
    description = Column(Text, nullable=True)

    # Relationships
    logs = relationship("Log", back_populates="service", cascade="all, delete-orphan")
    deployments = relationship("Deployment", back_populates="service", cascade="all, delete-orphan")
    incidents = relationship("Incident", back_populates="service", cascade="all, delete-orphan")
    metrics = relationship("Metric", back_populates="service", cascade="all, delete-orphan")


class Log(Base):
    """Represents application and infrastructure logs."""

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    level = Column(String(20), nullable=False, index=True)
    message = Column(Text, nullable=False)
    source = Column(String(100), nullable=True)

    # Relationships
    service = relationship("Service", back_populates="logs")


class Deployment(Base):
    """Represents deployment records."""

    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    version = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    status = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    service = relationship("Service", back_populates="deployments")


class Incident(Base):
    """Represents incident records."""

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="open")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # Relationships
    service = relationship("Service", back_populates="incidents")


class Metric(Base):
    """Represents operational metrics."""

    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=True)
    timestamp = Column(DateTime, nullable=False, index=True)

    # Relationships
    service = relationship("Service", back_populates="metrics")


class ApiError(Base):
    """Represents API errors for the API Agent."""

    __tablename__ = "api_errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    endpoint = Column(String(200), nullable=False)
    status_code = Column(Integer, nullable=False)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=False, index=True)

    # Relationships
    service = relationship("Service")


class DatabaseError(Base):
    """Represents database-related errors for the Database Agent."""

    __tablename__ = "database_errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True, index=True)
    error_type = Column(String(100), nullable=False)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=False, index=True)

    # Relationships
    service = relationship("Service")
