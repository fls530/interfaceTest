import os
import unittest
from requests import request
from Common.handle_path import DATA_DIR
from Library.myddt import ddt, data
from Common.handle_excel import HandleExcel
from Common.handle_config import conf
from Common.handle_logging import log
from Common.handle_assert import assert_dict

filename = os.path.join(DATA_DIR, "apitest.xlsx")


@ddt
class LoginTestCase(unittest.TestCase):
    excel = HandleExcel(filename, "login")
    cases = excel.read_data()

    @data(*cases)
    def test_login(self, case):
        method = case["method"]
        url = conf.get("env", "url") + case["url"]
        data = eval(case["data"])
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        res = (request(method, url, json=data)).json()
        try:
            assert_dict(expected, res)
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
