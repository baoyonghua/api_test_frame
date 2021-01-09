from common.baseyaml import BaseYaml
from config.pyfile_path import PyConfig


class YamlHandler(BaseYaml):
    pass


yaml = YamlHandler(PyConfig.yaml_path)
