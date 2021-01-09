"""
对项目进行审核的测试用例
"""

import json
import pytest

from common.baselogger import logger
from middleware.help import Context
from middleware.excel_handler import excel_handler
from middleware.yaml_handler import yaml
from middleware.help import replace_data

data = excel_handler.read_excel("audit")
host = yaml.read_yaml()["host"]["url"]


@pytest.mark.audit
@pytest.mark.usefixtures("init_req")
class TestAudit:

    @pytest.mark.parametrize("data_info", data)
    def test_audit(self, data_info, init_req):
        # 对excel中的数据进行替换
        data_info["data"] = replace_data("audit", data_info["data"])
        # 对excel中的带*号数据进行替换
        if "*loan_id*" in data_info["data"]:
            loan_id = Context(init_req).get_loan_id
            data_info["data"] = data_info["data"].replace("*loan_id*", loan_id)
        # 发送请求
        res = init_req.run_main(method=data_info["method"], url=host + data_info["url"],
                                data=json.loads(data_info["data"]))
        # 获取状态码
        code = res.json()["code"]
        # 进行断言
        try:
            # 1.状态码断言
            assert code == str(data_info["expected"])
            # 2.数据库中项目的status是否修改成功
            # ...
            # 将断言结果写入excel中
            excel_handler.write_excel("audit", data_info["case_id"] + 1, 9, "pass")
            logger.info("pass")
        except AssertionError as e:
            logger.exception("fail")
            excel_handler.write_excel("audit", data_info["case_id"] + 1, 9, "fail")
            raise e


if __name__ == '__main__':
    pytest.main(["-s", "-v", "-m", "audit"])
