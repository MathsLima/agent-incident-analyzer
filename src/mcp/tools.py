"""
MCP tools for accessing operational data.

These tools provide read-only access to simulated operational data stored in SQLite.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from src.database import get_db
from src.database.schema import (
    ApiError,
    DatabaseError,
    Deployment,
    Log,
    Metric,
    Service,
)


def get_service_status(service_name: str) -> dict:
    """
    Retrieve the current status of a service.

    Args:
        service_name: Name of the service.

    Returns:
        Dictionary with service status information.
    """
    db = get_db()
    session = db.get_session()

    try:
        service = session.query(Service).filter(
            Service.name == service_name
        ).first()

        if service is None:
            return {
                "error": f"Service '{service_name}' not found",
                "service_name": service_name,
            }

        return {
            "service_name": service.name,
            "status": service.status,
            "description": service.description,
        }
    finally:
        session.close()


def search_logs(
    service_name: str,
    level: Optional[str] = None,
    keyword: Optional[str] = None,
    limit: int = 50,
) -> dict:
    """
    Search logs associated with a service.

    Args:
        service_name: Name of the service.
        level: Log severity level (optional).
        keyword: Search term in message (optional).
        limit: Maximum number of results.

    Returns:
        Dictionary with matching logs.
    """
    db = get_db()
    session = db.get_session()

    try:
        query = session.query(Log).join(Service).filter(
            Service.name == service_name
        )

        if level:
            query = query.filter(Log.level == level.upper())

        if keyword:
            query = query.filter(Log.message.ilike(f"%{keyword}%"))

        logs = query.order_by(Log.timestamp.desc()).limit(limit).all()

        return {
            "service_name": service_name,
            "count": len(logs),
            "logs": [
                {
                    "timestamp": log.timestamp.isoformat(),
                    "level": log.level,
                    "message": log.message,
                    "source": log.source,
                }
                for log in logs
            ],
        }
    finally:
        session.close()


def get_api_errors(service_name: str, limit: int = 50) -> dict:
    """
    Retrieve recorded API errors.

    Args:
        service_name: Name of the service.
        limit: Maximum number of results.

    Returns:
        Dictionary with API errors.
    """
    db = get_db()
    session = db.get_session()

    try:
        errors = session.query(ApiError).join(Service).filter(
            Service.name == service_name
        ).order_by(ApiError.timestamp.desc()).limit(limit).all()

        return {
            "service_name": service_name,
            "count": len(errors),
            "errors": [
                {
                    "endpoint": error.endpoint,
                    "status_code": error.status_code,
                    "error_message": error.error_message,
                    "timestamp": error.timestamp.isoformat(),
                }
                for error in errors
            ],
        }
    finally:
        session.close()


def get_service_metrics(service_name: str, metric_name: Optional[str] = None) -> dict:
    """
    Retrieve simulated operational metrics.

    Args:
        service_name: Name of the service.
        metric_name: Name of the metric (optional).

    Returns:
        Dictionary with metrics.
    """
    db = get_db()
    session = db.get_session()

    try:
        query = session.query(Metric).join(Service).filter(
            Service.name == service_name
        )

        if metric_name:
            query = query.filter(Metric.name == metric_name)

        metrics = query.order_by(Metric.timestamp.desc()).all()

        return {
            "service_name": service_name,
            "count": len(metrics),
            "metrics": [
                {
                    "name": metric.name,
                    "value": metric.value,
                    "unit": metric.unit,
                    "timestamp": metric.timestamp.isoformat(),
                }
                for metric in metrics
            ],
        }
    finally:
        session.close()


def get_database_status(service_name: Optional[str] = None) -> dict:
    """
    Retrieve the simulated status of the database.

    Args:
        service_name: Name of the service (optional).

    Returns:
        Dictionary with database status.
    """
    db = get_db()
    session = db.get_session()

    try:
        if service_name:
            service = session.query(Service).filter(
                Service.name == service_name
            ).first()
            if service is None:
                return {
                    "error": f"Service '{service_name}' not found",
                    "service_name": service_name,
                }
            # Use the service as the database context
            db_service = service
        else:
            # Look for a database service
            db_service = session.query(Service).filter(
                Service.name.like("%database%")
            ).first()

        if db_service is None:
            return {
                "error": "Database service not found",
                "status": "unknown",
            }

        return {
            "service_name": db_service.name,
            "status": db_service.status,
            "description": db_service.description,
        }
    finally:
        session.close()


def get_database_errors(service_name: Optional[str] = None, limit: int = 50) -> dict:
    """
    Search for database-related errors.

    Args:
        service_name: Name of the service (optional).
        limit: Maximum number of results.

    Returns:
        Dictionary with database errors.
    """
    db = get_db()
    session = db.get_session()

    try:
        query = session.query(DatabaseError)

        if service_name:
            query = query.join(Service).filter(Service.name == service_name)

        errors = query.order_by(DatabaseError.timestamp.desc()).limit(limit).all()

        return {
            "service_name": service_name or "all",
            "count": len(errors),
            "errors": [
                {
                    "error_type": error.error_type,
                    "error_message": error.error_message,
                    "timestamp": error.timestamp.isoformat(),
                }
                for error in errors
            ],
        }
    finally:
        session.close()


def get_recent_deployments(service_name: str, limit: int = 10) -> dict:
    """
    Retrieve recent deployments.

    Args:
        service_name: Name of the service.
        limit: Maximum number of results.

    Returns:
        Dictionary with deployments.
    """
    db = get_db()
    session = db.get_session()

    try:
        deployments = session.query(Deployment).join(Service).filter(
            Service.name == service_name
        ).order_by(Deployment.timestamp.desc()).limit(limit).all()

        return {
            "service_name": service_name,
            "count": len(deployments),
            "deployments": [
                {
                    "version": deployment.version,
                    "timestamp": deployment.timestamp.isoformat(),
                    "status": deployment.status,
                    "description": deployment.description,
                }
                for deployment in deployments
            ],
        }
    finally:
        session.close()


def get_deployment_details(deployment_id: int) -> dict:
    """
    Retrieve details about a specific deployment.

    Args:
        deployment_id: Deployment identifier.

    Returns:
        Dictionary with deployment details.
    """
    db = get_db()
    session = db.get_session()

    try:
        deployment = session.query(Deployment).filter(
            Deployment.id == deployment_id
        ).first()

        if deployment is None:
            return {
                "error": f"Deployment with ID {deployment_id} not found",
                "deployment_id": deployment_id,
            }

        return {
            "deployment_id": deployment.id,
            "service_name": deployment.service.name,
            "version": deployment.version,
            "timestamp": deployment.timestamp.isoformat(),
            "status": deployment.status,
            "description": deployment.description,
        }
    finally:
        session.close()
