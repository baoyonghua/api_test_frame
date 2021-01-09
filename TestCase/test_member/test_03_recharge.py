"""
充值接口
"""
import json
from decimal import Decimal
import pytest
from jsonpath import jsonpath
from common.baselogger import logger
from middleware.excel_handler import excel_handler
from middleware.help import Context
from middleware.help import replace_data, get_phone
from middleware.yaml_handler import yaml


@pytest.mark.recharge
@pytest.mark.usefixtures("init_req")
class TestRecharge:
    host = yaml.read_yaml()["host"]["url"]
    data = excel_handler.read_excel("recharge")

    @pytest.mark.parametrize("data_info", data)
    def test_recharge(self, data_info, init_req):
        # 对excel中固定的数据进行替换
        data_info["data"] = replace_data("user_info", data_info["data"])
        # 对excel中异常的数据进行替换
        if "*mobilephone*" in data_info["data"]:
            phone = get_phone()
            data_info["data"] = data_info["data"].replace("*mobilephone*", phone)
        data = json.loads(data_info["data"])
        # 发送请求1获取获取请求前的金额
        before_amount = Context(init_req).leave_mount
        # 发送请求2
        res = init_req.run_main(data_info["method"], url=self.host + data_info["url"],
                                data=data)
        res = res.json()
        # 获取状态码和充值后返回数据中的金额
        code = res["code"]
        if code == "10001":
            after_amount = jsonpath(res, "$..leaveamount")[0]
            expected_amount = Decimal(before_amount) + Decimal(data["amount"])
        # 进行断言
        try:
            # 状态码断言
            assert code == str(data_info["expected"])
            # 返回数据中的金额断言
            if code == "10001":
                assert float(after_amount) == float(expected_amount)
            # 数据库断言
            # ....
            # 将断言结果写入excel
            excel_handler.write_excel("recharge", data_info["case_id"] + 1, 9, 'pass')
            logger.info('pass')
        except AssertionError as e:
            logger.exception("fail")
            excel_handler.write_excel("recharge", data_info["case_id"] + 1, 9, 'fail')
            raise e


if __name__ == '__main__':
    pytest.main(["-s", "-v", "-m", "recharge", "--reruns", "2", "--reruns-delay", "5"])
