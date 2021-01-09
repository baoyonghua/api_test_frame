"""
项目相关的db模块
"""
from common.basemysql import BaseMysql
from middleware.yaml_handler import yaml


class DbHandler(BaseMysql):
    pass


db_info = yaml.read_yaml()['db']
db = DbHandler()
# 连接数据库
db_handler = db.connect(host=db_info['host'], port=db_info['port'], user=db_info['user'], password=db_info['password'],
                        database=db_info['database'])