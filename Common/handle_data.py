import re
import jsonpath
from requests import request
from random import randint as R
from Common.handle_config import conf
from Common.handle_db import db


class EnvData:
    """定义一个类，用来保存用例执行过程中，提取出来的数据（当成环境变量的容器）"""
    pass


def login():
    """用例的前置条件：登录"""
    EnvData.name = random_proname()
    url = conf.get("env", "url") + "/user/login/"
    data = {
        "username": conf.get("test_data", "username"),
        "password": conf.get("test_data", "password")
    }
    res = (request(method="post", url=url, json=data)).json()
    token = "JWT" + " " + jsonpath.jsonpath(res, "$..token")[0]
    # 将提取出来的token作为EnvData的类属性（环境变量）
    setattr(EnvData, "token", token)


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


def random_proname():
    """生成一个数据库里面未注册的项目名称"""
    while True:
        name = "fls"
        for i in range(5):
            r = R(0, 9)
            name += str(r)
        # 数据库查询该用户名是否存在
        sql = 'SELECT * FROM test.tb_projects WHERE name="{}"'.format(name)
        res = db.find_count(sql)
        # 如果不存在,则返回该用户名
        if res == 0:
            return name
