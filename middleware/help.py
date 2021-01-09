"""
项目相关的帮助模块
"""
import os
import random
import json
import re
import time
from jsonpath import jsonpath
from common.baselogger import logger
from middleware.yaml_handler import yaml
from config.pyfile_path import PyConfig
from common.baserequest import BaseRequest


class Context:
    """
    上下文相关的数据存储
    """
    host = yaml.read_yaml()["host"]["url"]
    data = '{"mobilephone":"#mobilephone#","amount":"0"}'

    def __init__(self, session: BaseRequest):
        """

        :param session: 请求的session对象,
        """
        self.session = session

    def login(self):
        """
        登录请求
        :return:
        """
        # self.session.run_main()
        pass

    def recharge(self):
        """
        发送充值0元的请求
        :return:
        """
        data_info = replace_data("user_info", self.data)
        res = self.session.run_main('post', self.host + "/member/recharge", data=json.loads(data_info))
        return res.json()

    def get_loan_num(self):
        res = self.session.run_main(method="get", url=self.host + '/loan/getLoanList')
        loan_data = res.json()["data"]
        count = 0
        for i in loan_data:
            count += 1
        return count

    @property
    def get_loan_id(self):
        res = self.session.run_main(method="get", url=self.host + '/loan/getLoanList')
        loan_data = res.json()["data"]
        for loan in loan_data:
            if loan["status"] == "1":
                return loan["id"]

    @property
    def memberId(self):
        """
        获取用户ID
        :return:
        """
        # 调用充值接口
        res = self.recharge()
        member_id = jsonpath(res, "$..id")[0]
        return str(member_id)

    @property
    def leave_mount(self):
        res = self.recharge()
        leave_amount = jsonpath(res, "$..leaveamount")[0]
        return leave_amount


def sub_data(session, data_info):
    """
    利用正则替换哟用例中上下文关联的数据
    :param session:
    :param data_info:
    :return:
    """
    pattern = "@(.*?)@"
    while re.findall(pattern, data_info):
        key = re.search(pattern, data_info).group(1)
        try:
            data_info = re.sub(pattern, str(getattr(Context(session), key)), data_info, 1)
        except Exception as e:
            logger.error("替换excel表中上下关联的{}数据失败".format(key))
            raise e
    return data_info


def replace_data(yaml_key, data_info):
    """
    替换测试用例中固定的数据
    :return:
    """
    info = yaml.read_yaml()[yaml_key]
    pattern = "#(.*?)#"
    while re.findall(pattern, data_info):
        key = re.search(pattern, data_info).group(1)
        try:
            data_info = re.sub(pattern, str(info[key]), data_info, 1)
        except Exception as e:
            logger.error("替换excel表中固定的{}数据失败".format(key))
            raise e
    return data_info


def get_phone():
    """
    获取一个随机的手机号
    :return:
    """
    mobile: str = '1' + str(random.choice([3, 5, 7]))
    for i in range(9):
        mobile += str(random.randint(0, 9))
    logger.info("生成的手机号为：%s" % mobile)
    return mobile


def rm_log():
    """
    清除2天前的日志
    :return:
    """
    try:
        # 获取log目录下的log文件
        log_list = os.listdir(PyConfig.log_path)
    except FileNotFoundError as e:
        logger.error("文件路径错误")
        raise e
    length = len(log_list)
    while length > 0:
        for i in log_list:
            # 获取log文件的绝对路径
            path = r"%s\%s" % (PyConfig.log_path, i)
            # 获取log文件最后修改时的时间戳
            create = os.stat(path).st_mtime
            # 获取当前时间的时间戳
            now = time.time()
            # 进行判断是否大于两天
            if (now - create) / 24 / 60 / 60 > 2:
                try:
                    os.remove(path)
                except Exception as e:
                    logger.error("删除日志失败")
                    raise e
            length -= 1
        logger.info("没有2天前的日志了")


"""
cls 为类对象
cls作为键存储在instance字典中，值为它的内存地址
{cls : 内存地址}
"""


def singleton(cls):
    """单例模式装饰器"""
    instance = {}

    def inner(*args, **kwargs):
        if cls in instance:
            return instance[cls]
        else:
            instance[cls] = cls(*args, **kwargs)
            return instance[cls]
        return inner


if __name__ == '__main__':
    data = replace_data("user_info", '{"mobilephone":"-#mobilephone#","pwd":"#pwd#"}')
    # print(data)
    phone = get_phone()
    # print(phone)
    # rm_log()
    amount = Context(BaseRequest()).leave_mount
    memberId = Context(BaseRequest()).memberId
    # print(type(amount))
    # print(memberId)
    data = '{"memberId":"@memberId@","password":"#password#","loanId":"#loanId#","amount":"#amount#"}'
    data = sub_data(BaseRequest(), data)
    # print(data)
    loan_num = Context(BaseRequest()).get_loan_num()
    loan_id = Context(BaseRequest()).get_loan_id
    print(loan_id)
