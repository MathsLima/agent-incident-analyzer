"""
Seed database with demonstration data.
"""

from datetime import datetime, timedelta

from src.database.connection import get_db
from src.database.schema import (
    ApiError,
    DatabaseError,
    Deployment,
    Incident,
    Log,
    Metric,
    Service,
)


def seed_database() -> None:
    """Populate database with demonstration data."""
    db = get_db()
    session = db.get_session()

    # Clear existing data
    session.query(ApiError).delete()
    session.query(DatabaseError).delete()
    session.query(Metric).delete()
    session.query(Log).delete()
    session.query(Deployment).delete()
    session.query(Incident).delete()
    session.query(Service).delete()
    session.commit()

    # Create services
    payments_api = Service(
        name="payments-api",
        status="degraded",
        description="Payment processing API"
    )
    user_service = Service(
        name="user-service",
        status="healthy",
        description="User management service"
    )
    database = Service(
        name="main-database",
        status="unstable",
        description="Primary PostgreSQL database"
    )

    session.add_all([payments_api, user_service, database])
    session.commit()

    # Refresh to get IDs
    session.refresh(payments_api)
    session.refresh(user_service)
    session.refresh(database)

    # Create logs
    base_time = datetime.utcnow() - timedelta(hours=2)

    logs = [
        # payments-api logs
        Log(
            service_id=payments_api.id,
            timestamp=base_time + timedelta(minutes=10),
            level="ERROR",
            message="HTTP 500: Internal server error",
            source="payments-api"
        ),
        Log(
            service_id=payments_api.id,
            timestamp=base_time + timedelta(minutes=15),
            level="ERROR",
            message="DatabaseConnectionTimeout: Unable to connect to database",
            source="payments-api"
        ),
        Log(
            service_id=payments_api.id,
            timestamp=base_time + timedelta(minutes=20),
            level="ERROR",
            message="ConnectionPoolExhausted: No available connections",
            source="payments-api"
        ),
        Log(
            service_id=payments_api.id,
            timestamp=base_time + timedelta(minutes=25),
            level="WARN",
            message="High latency detected: 2.5s average response time",
            source="payments-api"
        ),
        # user-service logs
        Log(
            service_id=user_service.id,
            timestamp=base_time + timedelta(minutes=5),
            level="INFO",
            message="Service started successfully",
            source="user-service"
        ),
        Log(
            service_id=user_service.id,
            timestamp=base_time + timedelta(minutes=30),
            level="INFO",
            message="Request processed successfully",
            source="user-service"
        ),
    ]

    session.add_all(logs)
    session.commit()

    # Create deployments
    deployments = [
        Deployment(
            service_id=payments_api.id,
            version="2.4.1",
            timestamp=base_time + timedelta(minutes=5),
            status="completed",
            description="Updated payment processing logic"
        ),
        Deployment(
            service_id=user_service.id,
            version="1.8.0",
            timestamp=base_time - timedelta(hours=5),
            status="completed",
            description="Minor bug fixes"
        ),
    ]

    session.add_all(deployments)
    session.commit()

    # Create incidents
    incidents = [
        Incident(
            service_id=payments_api.id,
            title="Payment API returning HTTP 500 errors",
            description="Users unable to process payments",
            severity="high",
            status="open",
            created_at=base_time + timedelta(minutes=10),
        ),
        Incident(
            service_id=database.id,
            title="Database connection instability",
            description="Intermittent connection timeouts",
            severity="medium",
            status="open",
            created_at=base_time + timedelta(minutes=15),
        ),
    ]

    session.add_all(incidents)
    session.commit()

    # Create metrics
    metrics = [
        # payments-api metrics
        Metric(
            service_id=payments_api.id,
            name="error_rate",
            value=25.5,
            unit="percent",
            timestamp=base_time + timedelta(minutes=30),
        ),
        Metric(
            service_id=payments_api.id,
            name="latency",
            value=2500,
            unit="ms",
            timestamp=base_time + timedelta(minutes=30),
        ),
        Metric(
            service_id=payments_api.id,
            name="request_count",
            value=450,
            unit="requests/min",
            timestamp=base_time + timedelta(minutes=30),
        ),
        # user-service metrics
        Metric(
            service_id=user_service.id,
            name="error_rate",
            value=0.5,
            unit="percent",
            timestamp=base_time + timedelta(minutes=30),
        ),
        Metric(
            service_id=user_service.id,
            name="latency",
            value=120,
            unit="ms",
            timestamp=base_time + timedelta(minutes=30),
        ),
        # database metrics
        Metric(
            service_id=database.id,
            name="connection_pool_usage",
            value=95.0,
            unit="percent",
            timestamp=base_time + timedelta(minutes=30),
        ),
        Metric(
            service_id=database.id,
            name="query_latency",
            value=3200,
            unit="ms",
            timestamp=base_time + timedelta(minutes=30),
        ),
    ]

    session.add_all(metrics)
    session.commit()

    # Create API errors
    api_errors = [
        ApiError(
            service_id=payments_api.id,
            endpoint="/api/v1/payments/process",
            status_code=500,
            error_message="Internal server error",
            timestamp=base_time + timedelta(minutes=10),
        ),
        ApiError(
            service_id=payments_api.id,
            endpoint="/api/v1/payments/status",
            status_code=500,
            error_message="Database connection timeout",
            timestamp=base_time + timedelta(minutes=15),
        ),
        ApiError(
            service_id=payments_api.id,
            endpoint="/api/v1/payments/refund",
            status_code=503,
            error_message="Service unavailable",
            timestamp=base_time + timedelta(minutes=20),
        ),
    ]

    session.add_all(api_errors)
    session.commit()

    # Create database errors
    db_errors = [
        DatabaseError(
            service_id=payments_api.id,
            error_type="ConnectionTimeout",
            error_message="Unable to establish database connection",
            timestamp=base_time + timedelta(minutes=15),
        ),
        DatabaseError(
            service_id=payments_api.id,
            error_type="ConnectionPoolExhausted",
            error_message="No available connections in pool",
            timestamp=base_time + timedelta(minutes=20),
        ),
        DatabaseError(
            service_id=database.id,
            error_type="HighConnectionUsage",
            error_message="Connection pool at 95% capacity",
            timestamp=base_time + timedelta(minutes=25),
        ),
    ]

    session.add_all(db_errors)
    session.commit()

    session.close()
    print("✓ Database seeded with demonstration data")


if __name__ == "__main__":
    db = get_db()
    db.create_tables()
    seed_database()
