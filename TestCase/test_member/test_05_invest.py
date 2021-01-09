"""
投资接口测试用例

投资成功后，将生成一条投资记录保存到 invest 表，投资用户可用余额减少，并新增一条流水记录保存到 financeLog 表
"""
import pytest
import json
from decimal import Decimal
from middleware.excel_handler import excel_handler
from middleware.yaml_handler import yaml
from middleware.help import Context
from middleware.help import replace_data
from middleware.help import sub_data
from common.baselogger import logger
from common.baserequest import BaseRequest


@pytest.mark.invest
@pytest.mark.usefixtures("init_req")
class TestInvest:
    data = excel_handler.read_excel('invest')
    host = yaml.read_yaml()['host']['url']
    invest_info = yaml.read_yaml()["invest_info"]

    @pytest.mark.parametrize("data_info", data)
    def test_invest(self, init_req, data_info):
        # 对excel中的固定数据进行替换
        data_info["data"] = replace_data("user_info", data_info["data"])
        # 对excel中的上下关联数据进行替换
        data_info["data"] = sub_data(init_req, data_info["data"])
        # 将数据由json格式转换为字典形式
        data_info["data"] = json.loads(data_info["data"])
        # 发送请求1，获取投资前用户的可用余额
        before_amount = Context(init_req).leave_mount
        # 发送投资请求
        res = BaseRequest().run_main(method=data_info["method"], url=self.host + data_info["url"],
                                     data=data_info["data"])
        # 获取code
        res = res.json()
        code = res["code"]
        # 发送请求2，获取投资后用户的可用余额
        if code == '10001':
            after_amount = float(Context(init_req).leave_mount)
            amount = data_info["data"]["amount"]
            expected_amount = float(Decimal(before_amount) - Decimal(amount))
        # 进行断言
        try:
            # 断言1：状态码code断言
            assert code == json.loads(data_info["expected"])
            # 断言2：接口返回的金额断言
            if code == '10001':
                assert after_amount == expected_amount
            # 断言3：数据库中的用户金额断言
            # 断言4:invest 表是否新增一条投资记录
            # 断言5：是否新增一条流水记录保存到 financeLog 表
            # 将断言结果写入excel表中
            logger.info("pass")
            excel_handler.write_excel('invest', data_info["case_id"] + 1, 9, "pass")
        except AssertionError as e:
            logger.exception("fail")
            excel_handler.write_excel('invest', data_info["case_id"] + 1, 9, "fail")
            raise e


if __name__ == '__main__':
    pytest.main(["-s", "-v", "-m", "invest"])
