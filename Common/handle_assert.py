def assert_dict(expected, res):
    """
    自定义 用来对连个字典进行成员运算断言的方法
    :param expected: 预期结果
    :param res: 实际结果
    :return:
    """
    for key in expected:
        # 判断键是否存在,键对应的值也相等
        if key in res.keys() and expected[key] == res[key]:
            # 这个键对应的值是否一致,断言通过
            pass
        else:
            raise AssertionError("断言不通过!" + "预期结果:{},实际结果{}".format(expected, str(res)))
