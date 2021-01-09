"""
增加项目的测试用例
新增一个项目，借款人 id 必须是 member 表中已经存在，新增成功后，会保存一条项目记录到 loan 表中
发送请求获取所有的项目列表，查看是否新增了一个项目
"""
import pytest
import json

from common.baselogger import logger
from middleware.yaml_handler import yaml
from middleware.excel_handler import excel_handler
from middleware.help import replace_data
from middleware.help import sub_data
from middleware.help import Context

host = yaml.read_yaml()["host"]["url"]
data = excel_handler.read_excel('addloan')


@pytest.mark.add_loan
@pytest.mark.usefixtures("init_req")
class TestAdd:

    @pytest.mark.parametrize("data_info", data)
    def test_add_loan(self, init_req, data_info):
        # 对excel中的固定数据进行替换
        data_info["data"] = replace_data(yaml_key="add_loan", data_info=data_info["data"])
        # 对excel中上下文关联的数据进行替换
        data_info["data"] = sub_data(init_req, data_info["data"])
        # 发送请求1，获取创建项目前项目的总数
        before_loan_num = Context(init_req).get_loan_num()
        # 发送创建项目请求
        res = init_req.run_main(method=data_info["method"], url=host + data_info["url"],
                                data=json.loads(data_info["data"]))
        # 获取状态码
        code = res.json()["code"]
        if code == '10001':
            # 发送请求2，获取创建项目成功后项目的总数
            after_loan_num = Context(init_req).get_loan_num()
            expected_loan_num = before_loan_num + 1
        # 进行断言
        try:
            # 1.状态码断言
            assert code == str(data_info["expected"])
            if code == "10001":
                # 2.请求返回的项目总数断言
                assert after_loan_num == expected_loan_num
            # 3.数据库中的项目总数断言
            # ....
            # 将断言结果写入excel表中
            excel_handler.write_excel("addloan", data_info["case_id"] + 1, 9, "pass")
            logger.info("pass")
        except AssertionError as e:
            excel_handler.write_excel("addloan", data_info["case_id"] + 1, 9, "fail")
            logger.exception("fail")
            raise e


if __name__ == '__main__':
    pytest.main(["-s", "-v", "-m", "add_loan"])
