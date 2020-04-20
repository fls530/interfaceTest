import pymysql
from Common.handle_config import conf


class HandleMysql:
    """操作mysql数据库的类"""

    def __init__(self):
        """初始化方法中,连接到数据库"""
        self.con = pymysql.connect(host=conf.get("mysql", "host"),
                                   port=conf.getint("mysql", "port"),
                                   user=conf.get("mysql", "user"),
                                   password=conf.get("mysql", "password"),
                                   charset="utf8",
                                   cursorclass=pymysql.cursors.DictCursor)
        # 创建一个游标对象
        self.cur = self.con.cursor()

    def find_all(self, sql):
        """
        查询sql语句返回的所有数据
        :param sql: 查询的sql
        :return: 查询到的所有数据
        """
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def find_one(self, sql):
        """查询数据库获取到第一条数据"""
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def find_count(self, sql):
        """
        sql语句查询到的数据条数
        :param sql: 查询的sql
        :return:查询到的数据条数
        """
        self.con.commit()
        res = self.cur.execute(sql)
        return res

    def update(self, sql):
        """增删改操作的方法"""
        self.cur.execute(sql)
        self.con.commit()

    def close(self):
        self.cur.close()
        self.con.close()


db = HandleMysql()
