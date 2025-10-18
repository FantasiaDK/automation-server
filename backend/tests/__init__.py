from datetime import datetime, timedelta
from sqlmodel import Session

import app.database.models as models
import app.enums as enums

def generate_basic_data(session: Session):
    session.add(
        models.Credential(
            name="Secret credential",
            username="Secret username",
            password="My secret password",
            description="Test credential",
            deleted=False
        )
    )

    session.add(
        models.Credential(
            name="Secret deleted credential",
            username="Secret deleted username",
            password="My secret password",
            description="Test credential",
            deleted=True
        )
    )

    session.add(
        models.Asset(
            name="First Asset",
            description="First asset for testing",
            deleted=False
        )
    )

    session.add(
        models.Asset(
            name="First deleted asset",
            description="Test asset deleted",
            deleted=True
        )
    )

    session.add(
        models.Workqueue(
            name="Workqueue",
            description="Queue for unittest",
            enabled=True,
            deleted=False
        )
    )
    session.add(
        models.Workqueue(
            name="Deleted workqueue",
            description="Queue for unittest",
            enabled=True,
            deleted=True
        )
    )
    session.commit()

    session.add(
        models.WorkItem(
            status=enums.WorkItemStatus.NEW,
            data={},
            reference="Embedded workitem",
            locked=False,
            workqueue_id=1
        )
    )

    session.add(
        models.WorkItem(
            status=enums.WorkItemStatus.IN_PROGRESS,
            data={},
            reference="Embedded workitem",
            locked=False,
            workqueue_id=1
        )
    )

    session.add(
        models.WorkItem(
            status=enums.WorkItemStatus.COMPLETED,
            data={},
            reference="Embedded workitem",
            locked=False,
            workqueue_id=1
        )
    )

    session.add(
        models.WorkItem(
            status=enums.WorkItemStatus.FAILED,
            data={},
            reference="Embedded workitem",
            locked=False,
            workqueue_id=1
        )
    )

    session.add(
        models.WorkItem(
            status=enums.WorkItemStatus.PENDING_USER_ACTION,
            data={},
            reference="Embedded workitem",
            locked=False,
            workqueue_id=1
        )
    )

    session.commit()

    session.add(
        models.Process(
            name="Process",
            description="Process for unittest",
            target_type=enums.TargetTypeEnum.PYTHON,
            target_source="Some git url",
            target_credentials_id=1,
            credentials_id=1,
            workqueue_id=1,
            deleted=False,
        )
    )

    session.add(
        models.Process(
            name="Deleted process",
            description="Process for unittest",
            target_type=enums.TargetTypeEnum.PYTHON,
            target_source="Some git url",
            target_credentials_id=1,
            credentials_id=1,
            workqueue_id=1,
            deleted=True,
        )
    )

    session.add(
        models.Trigger(
            type=enums.TriggerType.CRON,
            cron="* * * * *",
            date=None,
            workqueue_id=None,
            enabled=True,
            process_id=1
        )
    )

    session.add(
        models.Trigger(
            type=enums.TriggerType.DATE,
            cron="",
            date=datetime.now() + timedelta(days=1),
            workqueue_id=None,
            enabled=True,
            process_id=1
        )
    )

    session.add(
        models.Trigger(
            type=enums.TriggerType.DATE,
            cron="",
            date=datetime.now() - timedelta(days=1),
            workqueue_id=None,
            enabled=True,
            deleted=True,
            last_triggered=datetime.now() - timedelta(days=1),
            process_id=1
        )
    )


    session.add(
        models.Trigger(
            type=enums.TriggerType.WORKQUEUE,
            cron="",
            date=None,
            workqueue_id=1,
            enabled=True,
            process_id=1
        )
    )

    session.add(
        models.Resource(
            name="resource",
            fqdn="resource.example.com",
            capabilities="win32 chrome python blue_prism",
            available=True,
            last_seen= datetime.now(),
            deleted=False,
        )
    )

    session.add(
        models.Resource(
            name="resource-old",
            fqdn="resource-old.example.com",
            capabilities="win32 chrome python blue_prism",
            available=False,
            last_seen=datetime.now() - timedelta(days=14),
            deleted=True,
        )
    )

    session.add(
        models.Resource(
            name="resource-should-expire",
            fqdn="resource-expire.example.com",
            capabilities="linux python",
            available=True,
            last_seen=datetime.now() - timedelta(minutes=11),
            deleted=False,
        )
    )

    session.add(
        models.Resource(
            name="resource-not-available",
            fqdn="resource-not-available.example.com",
            capabilities="win32 chrome python blue_prism",
            available=False,
            last_seen= datetime.now(),
            deleted=False,
        )
    )



    session.add(models.Session(process_id=1, status=enums.SessionStatus.NEW))

    session.add(
        models.Session(process_id=1, status=enums.SessionStatus.NEW, deleted=True)
    )

    session.add(
        models.Session(process_id=1, status=enums.SessionStatus.COMPLETED, deleted=False)
    )

    session.add(
        models.Session(process_id=1, status=enums.SessionStatus.NEW, deleted=False,resource_id=3, dispatched_at=datetime.now())
    )

    session.add(
        models.AuditLog(
            event_timestamp=datetime.now(),
            session_id=1,
            message="Test log",
            created_at=datetime.now(),
        )
    )
    
    session.add(
        models.AuditLog(
            event_timestamp=datetime.now(),
            session_id=1,
            workitem_id=1,
            message="Test log 2",
            created_at=datetime.now(),
        )
    )

    session.add(models.AuditLog(session_id=3, message="Test log 3", created_at=datetime.now(), event_timestamp=datetime.now()))
    session.add(models.AuditLog(session_id=3, message="Test log 3 - nothing to see here", created_at=datetime.now(), event_timestamp=datetime.now()))
    session.add(models.AuditLog(session_id=3, message="Test log 3", created_at=datetime.now(), event_timestamp=datetime.now()))

    session.commit()
