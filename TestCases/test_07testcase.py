import os
import unittest
import jsonpath
from requests import request
from random import randint as R
from Common.handle_path import DATA_DIR
from Library.myddt import ddt, data
from Common.handle_excel import HandleExcel
from Common.handle_config import conf
from Common.handle_db import db
from Common.handle_logging import log
from Common.handle_data import EnvData, replace_data
from Common.handle_assert import assert_dict

filename = os.path.join(DATA_DIR, "apitest.xlsx")


@ddt
class testcaseTestCase(unittest.TestCase):
    excel = HandleExcel(filename, "testcase")
    cases = excel.read_data()

    @classmethod
    def setUpClass(cls):
        """该测试类 所有用例执行之前的前置条件:登陆"""
        url = conf.get("env", "url") + "/user/login/"
        data = {
            "username": conf.get("test_data", "username"),
            "password": conf.get("test_data", "password")
        }
        res = (request(method="post", url=url, json=data)).json()
        token = "JWT" + " " + jsonpath.jsonpath(res, "$..token")[0]
        # 将提取出来的token作为EnvData的类属性（环境变量）
        EnvData.token = token

    def setUp(self):
        # 前置条件一: 创建一个新的项目,提取项目ID,保存为类属性
        url = conf.get("env", "url") + "/projects/"
        headers = {"Authorization": getattr(EnvData, "token")}
        data = {"name": testcaseTestCase.random_proname(),
                "leader": "fls530",
                "tester": "fls530",
                "programmer": "fls530",
                "publish_app": "test",
                "desc": "test"
                }
        # 发送项目请求,添加项目
        res = (request(method='post', url=url, json=data, headers=headers)).json()
        EnvData.pid = str(jsonpath.jsonpath(res, "$..id")[0])

        # 前置条件二: 创建一个新的接口,提取接口ID,保存为类属性
        url1 = conf.get("env", "url") + "/interfaces/"
        headers1 = {"Authorization": getattr(EnvData, "token")}
        idata = {"name": testcaseTestCase.random_intername(),
                 "tester": "fls530",
                 "project_id": EnvData.pid,
                 "desc": "test"}
        res1 = (request(method='post', url=url1, json=idata, headers=headers1)).json()
        EnvData.iid = str(jsonpath.jsonpath(res1, "$..id")[0])

    @data(*cases)
    def test_testcase(self, case):
        EnvData.name = testcaseTestCase.random_casename()
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        headers = {"Authorization": getattr(EnvData, "token")}
        data = eval(replace_data(case["data"]))
        expected = eval(replace_data(case["expected"]))
        row = case["case_id"] + 1
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            start_count = db.find_count(sql)
        res = (request(method=method, url=url, json=data, headers=headers)).json()
        try:
            assert_dict(expected, res)
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                end_count = db.find_count(sql)
                self.assertEqual(1, end_count - start_count)
        except AssertionError as e:
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value="未通过")
            raise e
        else:
            # 结果回写excel中
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")
    @staticmethod
    def random_proname():
        """生成一个数据库里面未注册的项目名"""
        while True:
            name = "pro"
            for i in range(5):
                r = R(0, 9)
                name += str(r)

            # 数据库查询该用户名是否存在
            # sql = "SELECT * From test.auth_user WHERE username ={}".format(name)
            sql = 'SELECT * FROM test.tb_projects WHERE name="{}"'.format(name)
            res = db.find_count(sql)
            # 如果不存在,则返回该用户名
            if res == 0:
                return name

    @staticmethod
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

    @staticmethod
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
