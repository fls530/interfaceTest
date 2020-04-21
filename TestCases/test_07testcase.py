import os
import unittest
from requests import request
from Common.handle_path import DATA_DIR
from Library.myddt import ddt, data
from Common.handle_excel import HandleExcel
from Common.handle_config import conf
from Common.handle_db import db
from Common.handle_logging import log
from Common.handle_data import EnvData, replace_data, login, newproject, newinterface, random_casename
from Common.handle_assert import assert_dict

filename = os.path.join(DATA_DIR, "apitest.xlsx")


@ddt
class testcaseTestCase(unittest.TestCase):
    excel = HandleExcel(filename, "testcase")
    cases = excel.read_data()

    @data(*cases)
    def test_testcase(self, case):
        login()
        newproject()
        newinterface()
        EnvData.name = random_casename()
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
