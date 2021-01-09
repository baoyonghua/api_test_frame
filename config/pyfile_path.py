import os
import time


class PyConfig:
    # 项目路径
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 日志文件夹路径
    log_path = os.path.join(base_path, 'log')
    # 日志文件路径
    log_name = time.strftime("%y-%m-%d %H_%M_%S")
    logfile_path = os.path.join(log_path, log_name + '.log')
    # config文件夹路径
    config_path = os.path.join(base_path, 'config')
    # yaml文件路径
    yaml_path = os.path.join(config_path, 'config.yaml')
    # excel文件路径
    data_dir_path = os.path.join(base_path, 'TestData')
    excel_path = os.path.join(data_dir_path, 'data.xlsx')


if __name__ == '__main__':
    py_file = PyConfig()
    # print(py_file.base_path)
