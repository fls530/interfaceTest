import re
import jsonpath
from requests import request
from random import randint as R
from Common.handle_config import conf
from Common.handle_db import db


class EnvData:
    """定义一个类，用来保存用例执行过程中，提取出来的数据（当成环境变量的容器）"""


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


def newproject():
    # 每条用例之前都添加一个新的项目
    url = conf.get("env", "url") + "/projects/"
    headers = {"Authorization": getattr(EnvData, "token")}
    data = {"name": random_proname(),
            "leader": "fls530",
            "tester": "fls530",
            "programmer": "fls530",
            "publish_app": "test",
            "desc": "test"
            }
    # 发送项目请求,添加项目
    res = (request(method='post', url=url, json=data, headers=headers)).json()
    EnvData.pid = str(jsonpath.jsonpath(res, "$..id")[0])


def newinterface():
    url = conf.get("env", "url") + "/interfaces/"
    headers = {"Authorization": getattr(EnvData, "token")}
    data = {"name": random_intername(),
            "tester": "fls530",
            "project_id": getattr(EnvData, "pid"),
            "desc": "test"}
    res = (request(method='post', url=url, json=data, headers=headers)).json()
    EnvData.iid = str(jsonpath.jsonpath(res, "$..id")[0])


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


def random_intername():
    """生成一个数据库里面未注册的接口名"""
    while True:
        name = "inter"
        for i in range(5):
            r = R(0, 9)
            name += str(r)

        # 数据库查询该用户名是否存在
        # sql = "SELECT * From test.auth_user WHERE username ={}".format(name)
        sql = 'SELECT * FROM test.tb_interfaces WHERE name="{}"'.format(name)
        res = db.find_count(sql)
        # 如果不存在,则返回该用户名
        if res == 0:
            return name


def random_casename():
    """生成一个数据库里面未注册的用例名"""
    while True:
        name = "case"
        for i in range(5):
            r = R(0, 9)
            name += str(r)

        # 数据库查询该用户名是否存在
        # sql = "SELECT * From test.auth_user WHERE username ={}".format(name)
        sql = 'SELECT * FROM test.tb_testcases WHERE name="{}"'.format(name)
        res = db.find_count(sql)
        # 如果不存在,则返回该用户名
        if res == 0:
            return name
