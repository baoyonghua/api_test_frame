"""
请求类的基类
"""
import requests

from common.baselogger import logger


class BaseRequest:
    """
    请求类的基类
    """

    def __init__(self):
        self.session = requests.session()

    def send(self, method, url, headers=None, data=None, json=None, params=None, **kwargs):
        """
        发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param headers: 请求头信息
        :param data: 请求数据，data类型
        :param json: 请求数据，json类型
        :param params: 请求数据，get
        :param kwargs:
        :return: json
        """
        res = self.session.request(method=method, url=url, params=params, data=data, headers=headers, json=json,
                                   **kwargs)
        return res

    def run_main(self, method, url, headers=None, data=None, json=None, params=None, **kwargs):
        """
        调用主函数发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param headers: 请求头信息
        :param data: 请求数据，data类型
        :param json: 请求数据，json类型
        :param params: 请求数据，get
        :param kwargs:
        :return: res.json()
        """
        try:
            reason = self.send(method=method, url=url, headers=headers, data=data, json=json, params=params, **kwargs)
        except Exception as e:
            logger.exception("调用主函数失败")
            raise e
        return reason

    def close(self):
        """
        关闭session对象
        :return:
        """
        if self.session:
            self.session.close()
            return True


# if __name__ == '__main__':
#     req = BaseRequest()
#     res = req.run_mian('get', "https://www.baidu.com")
#     print(res)
