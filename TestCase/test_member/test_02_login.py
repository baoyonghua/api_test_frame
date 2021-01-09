"""
登录接口用例
"""
import pytest
import json
from common.baselogger import logger
from middleware.help import replace_data
from middleware.excel_handler import excel_handler
from middleware.yaml_handler import yaml
from middleware.help import get_phone


@pytest.mark.login
@pytest.mark.usefixtures("init_req")
class TestLogin:
    host = yaml.read_yaml()['host']['url']
    data = excel_handler.read_excel('login')

    @pytest.mark.parametrize("data_info", data)
    def test_login(self, init_req, data_info):
        # 对excel中固定的数据进行替换
        data_info["data"] = replace_data("user_info", data_info["data"])
        # 对excel中的异常数据进行替换
        if "*mobilephone*" in data_info["data"]:
            phone = get_phone()
            data_info["data"] = data_info["data"].replace("*mobilephone*", phone)
        # 发送请求
        res = init_req.run_main(method=data_info["method"], url=self.host + data_info["url"],
                                data=json.loads(data_info["data"]))
        # 获取code
        code = res.json()["code"]
        # 进行断言
        try:
            # 断言状态码
            assert code == str(data_info["expected"])
            # 断言结果写入excel
            excel_handler.write_excel('login', data_info["case_id"] + 1, 9, "PASS")
            logger.info("PASS")
        except AssertionError as e:
            logger.exception("FAIL")
            excel_handler.write_excel('login', data_info["case_id"] + 1, 9, "FAIL")
            raise e


if __name__ == '__main__':
    pytest.main(["-s", "-v", "-m", "login", "--reruns", "2", "--reruns-delay", "5"])
