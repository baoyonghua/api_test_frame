"""
注册接口用例
"""
import json
import pytest
from middleware.yaml_handler import yaml
from middleware.excel_handler import excel_handler
from common.baselogger import logger
from middleware.help import replace_data, get_phone


@pytest.mark.register
@pytest.mark.usefixtures("init_req")
class TestRegister:
    data = excel_handler.read_excel('registe')
    host = yaml.read_yaml()['host']['url']

    @pytest.mark.parametrize("data_info", data)
    def test_register(self, init_req, data_info):
        # 对excel中的固定的数据进行替换
        data_info["data"] = replace_data("user_info", data_info["data"])
        # 对excel中的不固定数据进行替换
        if "*phone*" in data_info["data"]:
            phone = get_phone()
            data_info["data"] = data_info["data"].replace("*phone*", phone)
        # 发送请求
        result = init_req.run_main(method=data_info['method'], url=self.host + data_info["url"],
                                   data=json.loads(data_info["data"]))
        # 获取状态码
        code = result.json()["code"]
        try:
            # 进行断言
            # 1.状态码断言
            assert code == str(data_info["expected"])
            # 2.查看数据库是否新增对应的新用户
            # ...
            logger.info("PASS")
            excel_handler.write_excel('registe', data_info["case_id"] + 1, 9, "pass")
        except AssertionError as e:
            logger.error("FAIL")
            excel_handler.write_excel('registe', data_info["case_id"] + 1, 9, "fail")
            raise e


if __name__ == '__main__':
    pytest.main(["-s", "-v", "-m", "register", "--reruns", "2", "--reruns-delay", "5"])
