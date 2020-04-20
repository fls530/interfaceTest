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
class ProjectTestCase(unittest.TestCase):
    excel = HandleExcel(filename, "project")
    cases = excel.read_data()

    @classmethod
    def setUpClass(cls):
        """用例的前置条件：登录"""
        url = conf.get("env", "url") + "/user/login/"
        data = {
            "username": conf.get("test_data", "username"),
            "password": conf.get("test_data", "password")
        }
        res = (request(method="post", url=url, json=data)).json()
        print(res)
        token = "JWT" + " " + jsonpath.jsonpath(res, "$..token")[0]
        # 将提取出来的token作为EnvData的类属性（环境变量）
        setattr(EnvData, "token", token)
        EnvData.name = ProjectTestCase.random_username()

    @data(*cases)
    def test_project(self, case):
        # 准备用例数据
        method = case["method"]
        url = conf.get("env", "url") + case["url"]
        headers = {"Authorization": getattr(EnvData, "token")}
        data = eval(replace_data(case["data"]))
        expected = eval(replace_data(case["expected"]))
        row = case["case_id"] + 1
        # 创建项目之前，查询数据库中的项目数量
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            start_count = db.find_count(sql)
        # 第二步，发送请求获取实际结果
        res = (request(method, url, json=data, headers=headers)).json()
        # 第三步，断言预期结果和实际结果
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
    def random_username():
        """生成一个数据库里面未注册的项目名"""
        while True:
            name = "fls"
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
