"""
Description:
Version: 2.0
Autor: byh
Date: 2021-01-03 21:19:14
LastEditors: byh
LastEditTime: 2021-01-03 22:50:22
"""
import pytest
from common.baserequest import BaseRequest
from middleware.help import rm_log
from common.baselogger import logger


@pytest.fixture()
def init_req():
    req = BaseRequest()
    yield req
    req.close()


@pytest.fixture(scope="session", autouse=True)
def init_data_clean():
    logger.info("******开始执行测试用例******")
    rm_log()
    yield
    logger.info("******测试用例执行完毕******")


@pytest.fixture(scope="session", autouse=True)
def init_db():
    pass
