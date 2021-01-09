import pymysql
from common.baselogger import logger
from pymysql.cursors import DictCursor


class BaseMysql:

    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self, host, port, user, password, database, charset="utf8", cursorclass=DictCursor, **kwargs):
        """
        连接数据库
        :param host: 主机地址
        :param port: 端口号
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名称
        :param charset: 字符编码
        :param cursorclass: 设置输出格式为字典格式
        :param kwargs:
        :return: True/False
        """
        try:
            self.conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                        charset=charset,
                                        cursorclass=cursorclass, **kwargs)
        except Exception as e:
            logger.error("连接数据库失败 {}".format(e))
            raise e
        self.cur = self.conn.cursor()
        return self

    def select(self, sql, args=[], one=True):
        """
        查询数据库
        :param one:
        :param sql: sql语句
        :param args: sql参数
        :return: 执行结果
        """
        if self.conn and self.cur:
            try:
                self.cur.execute(sql, args)
            except Exception as e:
                logger.exception("执行sql失败 {}{}".format(sql, args))
                raise e
            if one:
                res = self.cur.fetchone()
                self.conn.commit()
            else:
                res = self.cur.fetchall()
                self.conn.commit()
            logger.info("执行sql成功 {}".format(sql, args))
            return res
        else:
            return "未连接数据库"

    def execute(self, sql):
        """
        执行sql，主要用于写入操作
        :param sql: sql语句
        :return: True/False
        """
        if self.conn and self.cur:
            try:
                self.cur.execute(sql)
            except Exception as e:
                logger.error("执行sql失败{}".format(sql))
                raise e
            self.conn.commit()
            logger.info("执行sql成功{}".format(sql))
            return True

    def close(self):
        """
        关闭数据库
        :return:T/F
        """
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
            logger.info("关闭数据库成功")
            return True
        else:
            return False
