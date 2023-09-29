import pprintpp
import pytest
from faker import Faker

fake = Faker()


@pytest.fixture(scope='session')
def faker():
    # global fake
    yield fake


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    __builtins__['pp'] = pprintpp.PrettyPrinter(width=41)
    # code before tests run
    yield
    del __builtins__['pp']
    # code after tests run


@pytest.fixture(scope='session')
def celery_task_always_eager(celery_worker):
    return True
