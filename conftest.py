"""
Used to store all the fixtures. Any fixtures defined here are available for all the tests.
"""
import os
import pytest

try:
    from .temp_env_var import TEMP_ENV_VARS, ENV_VARS_TO_SUSPEND
except ImportError:
    TEMP_ENV_VARS = {}
    ENV_VARS_TO_SUSPEND = []


@pytest.fixture(scope="session", autouse=True)
def tests_setup_and_teardown():
    # Will be executed before the first test
    old_environ = dict(os.environ)
    os.environ.update(TEMP_ENV_VARS)
    for env_var in ENV_VARS_TO_SUSPEND:
        os.environ.pop(env_var, default=None)

    yield
    # Will be executed after the last test
    os.environ.clear()
    os.environ.update(old_environ)