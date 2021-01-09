import logging
from config.pyfile_path import PyConfig


class BaseLogger(logging.Logger):
    """
    日志模块的基类
    """

    def __init__(self, file_path=None, name='root', level='DEBUG'):
        super().__init__(name)
        self.setLevel(level)
        fmt = logging.Formatter("%(asctime)s - %(levelno)s - %(filename)s - %(lineno)d - %(name)s - "
                                "%(levelname)s - %(message)s")
        if not file_path:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            stream_handler.setFormatter(fmt)
            self.addHandler(stream_handler)
        else:
            file_handler = logging.FileHandler(file_path, encoding='utf8')
            file_handler.setLevel(level)
            file_handler.setFormatter(fmt)
            self.addHandler(file_handler)


logger = BaseLogger(file_path=PyConfig.logfile_path)

