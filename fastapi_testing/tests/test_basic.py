import pytest
import unittest


class TestSomethingSimple(unittest.TestCase):

    def test_some_simple_test(self):
        assert True


class AsyncTestSimple(unittest.IsolatedAsyncioTestCase):
    @pytest.mark.asyncio
    async def test_asyncio(self):
        return True