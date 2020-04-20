import os
from configparser import ConfigParser
from Common.handle_path import CONF_DIR


class HandleConfig(ConfigParser):
	"""配置文件解析器的封装"""

	def __init__(self, filename):
		super().__init__()
		self.read(filename, encoding="utf8")


conf = HandleConfig(os.path.join(CONF_DIR, "config.ini"))
