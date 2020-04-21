import os
import unittest
import requests
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
class RegisterTestCase(unittest.TestCase):
    excel = HandleExcel(filename, "register")
    cases = excel.read_data()

    @data(*cases)
    def test_register(self, case):
        # 准备用例数据
        method = case["method"]
        url = conf.get("env", "url") + case["url"]
        if case["interface"] == "register":
            # 注册接口，则随机生成一个用户名和email
            EnvData.name = self.random_username()
            EnvData.email = self.random_email()
        data = eval(replace_data(case["data"]))
        expected = eval(replace_data(case["expected"]))
        row = case["case_id"] + 1
        # 第二步:发送请求获取实际结果
        res = (requests.request(method=method, url=url, json=data)).json()
        # 第三步：断言
        try:
            assert_dict(expected, res)
            # 判断是否需要进行sql校验
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                res = db.find_count(sql)
                self.assertEqual(1, res)
        except AssertionError as e:
            # 结果回写excel中
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
        """生成一个数据库里面未注册的用户名"""
        while True:
            name = "fls"
            for i in range(5):
                r = R(0, 9)
                name += str(r)

            # 数据库查询该用户名是否存在
            sql = 'SELECT * FROM test.auth_user WHERE username="{}"'.format(name)
            res = db.find_count(sql)
            # 如果不存在,则返回该用户名
            if res == 0:
                return name

    @staticmethod
    def random_email():
        """生成一个数据库里面未注册的邮箱地址"""
        while True:
            num = ""
            address = ""
            email = "@qq.com"
            for i in range(9):
                r = R(0, 9)
                num += str(r)
                address = num + email
            # 数据库查询该用户名是否存在
            sql = 'SELECT * from test.auth_user WHERE email ="{}"'.format(address)
            res = db.find_count(sql)
            # 如果不存在,则返回该用户名
            if res == 0:
                return address
