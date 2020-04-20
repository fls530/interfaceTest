import os

# 获取项目所在的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

# 用例模块所在的目录路径
CASE_DIR = os.path.join(BASE_DIR, "TestCases")

# 用例数据所在的目录路径
DATA_DIR = os.path.join(BASE_DIR, "Data")

# 配置文件所在的目录路径
CONF_DIR = os.path.join(BASE_DIR, "Conf")

# 测试报告所在的目录路径
REPORT_DIR = os.path.join(BASE_DIR, "Reports")

# 日志文件所在的目录路径
LOG_DIR = os.path.join(BASE_DIR, "Logs")
