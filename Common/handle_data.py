import re
from Common.handle_config import conf


class EnvData:
    """定义一个类，用来保存用例执行过程中，提取出来的数据（当成环境变量的容器）"""
    pass


def replace_data(data):
    """替换数据"""
    while re.search("#(.*?)#", data):
        res = re.search("#(.*?)#", data)
        key = res.group()
        item = res.group(1)
        try:
            # 获取配置文件中的测试数据
            value = conf.get("test_data", item)
        except:
            value = getattr(EnvData, item)

        data = data.replace(key, value)
    return data
