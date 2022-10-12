import xlrd

# class point():
#     def __init__(self, )
class dataset():
    def __init__(self, path, sheet):
        self.path = path
        self.sheet = sheet
        if sheet == "excel3.xlsx":
            self.load3()

    def load3(self):
        # 得到excel的句柄
        wb = xlrd.open_workbook(self.path + self.sheet)

        # 获得excel表的信息
        sheet_num = wb.nsheets
        sheet_names = wb.sheet_names()

        sheet = wb.sheet_by_index(2)
        rows=sheet.nrows   #获取sheet页的行数，一共有几行
        columns=sheet.ncols   #获取sheet页的列数，一共有几列
        
        # 小区编号
        self.comm_index = list(map(int, sheet.col_values(0)[1:]))
        # 小区人口数
        self.comm_people_nums = list(map(int, sheet.col_values(3)[1:]))
        # 横坐标
        self.comm_x_axis = list(map(float, sheet.col_values(4)[1:]))
        # 纵坐标
        self.comm_y_axis = list(map(float, sheet.col_values(5)[1:]))
              
        self.comm_nums = len(self.comm_index)
        
        comm_loca = sheet.col_values(7)

        self.comm_loca_index = dict([(k, 0) for k in range(9)])
        j = -1
        for i in range(1, len(comm_loca)):
            if comm_loca[i] != comm_loca[i-1]:
                j += 1
            self.comm_loca_index[j] += 1

        # 将每个小区按照区划分
        """
        宽城区      C
        二道区      E
        朝阳区      A
        绿园区      D
        南关区      B
        经开区      G
        长春新区(高新 F
        净月区      H
        汽开区      I
        """
    
        one_data = sheet.cell(0,0)
    def load2(self):
        # 读取长春市投放点和人数的关系
        wb2 = xlrd.open_workbook(self.path + self.sheet)

        sheet2 = wb2.sheet_by_index(0)

        in_people = sheet2.col_values(1)
        point_nums = list(map(int, sheet2.col_values(2)[1:]))
        print(sum(point_nums))

if __name__ == "__main__":
    abs_path = "/Users/candy/Documents/资源/研究生工作/浙江理工/数学建模/code/data/"
    path = "./data/"
    sheet = "excel3.xlsx"
    data = dataset(
        path=abs_path,
        sheet=sheet
    )
    # label = []
    # for i in range(9):
    #     label = label + [i] * data.comm_loca_index[i]
    # print(label)
    for i in range(9):
        print(data.comm_loca_index[i])