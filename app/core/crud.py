from sqlalchemy.orm import Session
from .models import Test
import uuid
from typing import Optional


def get_test(db: Session, test_id: uuid.UUID) -> Optional[Test]:
    return db.query(Test).filter(Test.id == test_id).first()
