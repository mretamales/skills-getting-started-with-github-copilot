import copy

import pytest

from src import app as app_module

DEFAULT_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activity database before every test."""
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(DEFAULT_ACTIVITIES))
    yield
