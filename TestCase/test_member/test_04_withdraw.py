"""
取现接口测试用例
"""
import pytest
import json
from jsonpath import jsonpath
from decimal import Decimal
from common.baselogger import logger
from middleware.yaml_handler import yaml
from middleware.excel_handler import excel_handler
from middleware.help import replace_data
from middleware.help import get_phone
from middleware.help import Context


@pytest.mark.withdraw
@pytest.mark.usefixtures("init_req")
class TestWithdraw:
    data = excel_handler.read_excel('withdraw')
    host = yaml.read_yaml()["host"]["url"]

    @pytest.mark.parametrize("data_info", data)
    def test_withdraw(self, init_req, data_info):
        # 对excel中固定的数据进行替换
        data_info["data"] = replace_data("user_info", data_info["data"])
        # 对excel中不固定的数据进行替换（new_phone）
        if "*mobilephone*" in data_info["data"]:
            new_phone = get_phone()
            data_info["data"] = data_info["data"].replace("*mobilephone*", new_phone)
        data_info["data"] = json.loads(data_info["data"])
        # 发送请求1，获取接口返回的初始金额
        before_amount = Context(init_req).leave_mount
        # 发送取现请求
        res = init_req.run_main(method=data_info["method"], url=self.host + data_info["url"], data=data_info["data"])
        res = res.json()
        # 获取状态码code
        code = res["code"]
        if code == "10001":
            # 获取接口返回的取现后的金额
            after_amount = jsonpath(res, "$..leaveamount")[0]
            # 获取充值金额
            amount = data_info["data"]["amount"]
            # 预期金额
            expected_amount = Decimal(before_amount) - Decimal(amount)
        # 进行断言
        try:
            # 断言1：状态码断言
            assert code == data_info["expected"]
            # 断言2：接口返回的金额断言
            if code == "10001":
                assert float(after_amount) == float(expected_amount)
            # 断言3：数据库断言
            # ...
            # 将断言结果写入excel表中
            excel_handler.write_excel("withdraw", data_info["case_id"] + 1, 9, "pass")
            logger.info("pass")
        except AssertionError as e:
            logger.exception("fail")
            # 将断言结果写入excel表中
            excel_handler.write_excel("withdraw", data_info["case_id"] + 1, 9, "fail")
            raise e


if __name__ == '__main__':
    pytest.main(["-s", "-v", "-m", "withdraw", "--reruns", "2", "--reruns-delay", "5"])
