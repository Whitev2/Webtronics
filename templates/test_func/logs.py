import asyncio

import aiohttp
from io import StringIO
import sys


async def logs(cont, name):
    conn = aiohttp.UnixConnector(path="/var/run/docker.sock")
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(f"http://xx/containers/{cont}/logs?follow=1&stdout=1") as resp:
            async for line in resp.content:
                print(name, line)


class OutputInterceptor(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


async def test_data(cont, name):
    """
    Тестовая функция для вывода данных
    """
    print(name, "INFO: line1")
    print(name, "INFO: line1")
    print(name, "INFO: line1")
    print(name, "INFO: line1")
    print(name, "INFO: line1")


def interceptor(cont, name):
    with OutputInterceptor() as output:
        asyncio.run(test_data(cont, name))

        # await logs(cont, name")

    return output


def test_debug_level():
    for log in interceptor(777, "dev"):
        assert "INFO" in log


def test_name():
    for log in interceptor(777, "dev"):
        assert "dev" in log
