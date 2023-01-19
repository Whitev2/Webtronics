import asyncio
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


async def generator(cont, name):
    for i in range(10):
        yield (name, f"INFO: line {i}")
        await asyncio.sleep(0.4)


async def test_data(cont, name):
    """
    Заменяет асинхронный циклв тестовой функции
    """
    async for i, b in generator(cont, name):
        print(i, b)


def interceptor():
    """
    Вызывает test_data в двух потоках
    """
    with OutputInterceptor() as output:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.gather(test_data("1", "multithread_1"), test_data("2", "multithread_2")))
        finally:
            loop.close()

        # await logs(cont, name")

    return output


def test_debug_level():
    for log in interceptor():
        assert "INFO" in log


def test_name():
    for log in interceptor():
        assert "multithread" in log
