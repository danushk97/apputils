from datetime import datetime
from freezegun import freeze_time

from appscommon.domain.models.basemodel import BaseModel


@freeze_time('1/1/2023')
def test_basemodel_returns_basemodel_instance():
    base_model = BaseModel(
        'fake_id',
        datetime.now(),
        None,
        None,
        True
    )
    assert base_model.created_by == 'fake_id'
    assert base_model.created_at.date() == datetime(2023, 1, 1).date()
    assert base_model.last_updated_at is None
    assert base_model.last_updated_by is None
    assert base_model.is_active is True
