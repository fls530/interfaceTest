import openpyxl


class HandleExcel:
    """用来操作excel文件的类"""

    def __init__(self, filename, sheetname):
        """

        :param filename: excel文件路径
        :param sheetname: 表单名
        """
        self.filename = filename
        self.sheetname = sheetname
        """将加载文件和获取表单名,写进初始化方法"""
        self.wb = openpyxl.load_workbook(self.filename)
        self.sh = self.wb[self.sheetname]

    def read_data(self):
        """读取excel中的数据"""

        # 按行获取所有的数据,转换为列表
        row_data = list(self.sh.rows)
        # 创建一个空列表用例保存所有的用例数据
        case_data = []
        # 获取表单中的表头数据,放入title中
        title = []
        for i in row_data[0]:
            title.append(i.value)

        # 获取除表头之外的其他行数据
        for item in row_data[1:]:
            # 每遍历出来一行数据,就创造一个空列表,来存放该行数据
            values = []
            for i in item:
                values.append(i.value)
            # 将该行的数据和表头进行打包,转换为字典
            case = dict(zip(title, values))
            case_data.append(case)
        return case_data

    def write_data(self, row, column, value):
        """
        写入数据
        :param row: 行
        :param column: 列
        :param value: 写入的值
        :return:
        """
        self.sh.cell(row=row, column=column, value=value)
        self.wb.save(self.filename)


if __name__ == '__main__':
    excel = HandleExcel(r"C:\Users\Administrator\Desktop\interfacetest\Data\apitest.xlsx", "register")
    excel.write_data(row=1, column=1, value="python")
