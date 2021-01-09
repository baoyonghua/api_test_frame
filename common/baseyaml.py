import yaml

from common.baselogger import logger


class BaseYaml:
    """
    操作yaml文件基类
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def read_yaml(self):
        try:
            with open(self.file_path, mode='r', encoding='utf8') as f:
                res = yaml.load(stream=f, Loader=yaml.FullLoader)
        except Exception as e:
            logger.exception("读取yaml文件失败")
            raise e
        # logger.info("读取yaml文件成功,数据为：{}".format(res))
        return res

    def write_yaml(self, data):
        try:
            with open(self.file_path, mode='w', encoding='utf8') as f:
                yaml.dump(stream=f, data=data, allow_unicode=True)
        except Exception as e:
            logger.exception("写入yaml文件失败")
            raise e
        logger.info("写入yaml文件成功 {}".format(data))
        return True


if __name__ == '__main__':
    pass
