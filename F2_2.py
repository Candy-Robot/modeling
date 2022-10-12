import pandas as pd
import numpy as np
import load_data
import matplotlib.pyplot as plt

from utils import draw_plt, xw_toExcel

# 计算中心点到各点距离
def center_distence(x, y, x_list, y_list):
	D = []
	for i in range(len(x_list)):
		D.append(pow(pow(x - x_list[i], 2) + pow(y - y_list[i], 2), 0.5))
	return D

#对单组使用单重心法得到重心坐标
def single_point(volume_list, x_list, y_list):
	# 计算初始中心
	def first_center(volume_list, x_list, y_list):
		x0 = sum(np.multiply(volume_list, x_list)) / sum(volume_list)
		y0 = sum(np.multiply(volume_list, y_list)) / sum(volume_list)
		return x0, y0

	# # 计算中心点到各点距离
	# def center_distence(x, y, x_list, y_list):
	# 	D = []
	# 	for i in range(len(x_list)):
	# 		D.append(pow(pow(x - x_list[i], 2) + pow(y - y_list[i], 2), 0.5))
	# 	return D

	# 计算新中心点
	def new_center(volume_list, x_list, y_list, D):
		x_new = sum(np.divide(np.multiply(volume_list, x_list), D)) / sum(np.divide(volume_list, D))
		y_new = sum(np.divide(np.multiply(volume_list, y_list), D)) / sum(np.divide(volume_list, D))
		return x_new, y_new

	zuobiao = []
	# （1）计算初始中心点
	x0, y0 = first_center(volume_list, x_list, y_list)
	zuobiao.append([x0, y0])

	# （2）计算中心点到各点距离
	D = center_distence(x0, y0, x_list, y_list)

	# （3）修正中心坐标值
	x_new, y_new = new_center(volume_list, x_list, y_list, D)
	zuobiao.append([x_new, y_new])

	#循环计算重心，直到两次迭代精度差<0.01
	while abs(zuobiao[len(zuobiao) - 1][0] - zuobiao[len(zuobiao) - 2][0]) > 0.01:
		# 重复（2）计算中心点到各点距离
		D = center_distence(x_new, y_new, x_list, y_list)
		# 重复（3）修正中心坐标值
		x_new, y_new = new_center(volume_list, x_list, y_list, D)
		zuobiao.append([x_new, y_new])

	#返回重心坐标
	return zuobiao[len(zuobiao)-1]

# 计算每个人领取物资需要走的总和
def trans_cost(x, y, volume_list, x_list, y_list):
	D = center_distence(x, y, x_list, y_list)
	return np.multiply(volume_list, D)

class comm():
    def __init__(self, people_nums, x, y) :
        self.people_nums = people_nums
        self.x = x
        self.y = y

if __name__ == '__main__':
    abs_path = "/Users/candy/Documents/资源/研究生工作/浙江理工/数学建模/code/data/"
    path = "./data/"
    sheet = "excel3.xlsx"
    data = load_data.dataset(
        path=abs_path,
        sheet=sheet
    )
    # 设置需要多少个供应点
    POINT_NUMS = 9
    EPOCH = 10000
    point_nums = POINT_NUMS
    plt_save = str(point_nums) + 'point.png'
    
    # 初始化
    volume_nums = int(data.comm_nums / point_nums)
    people_dict, x_dict, y_dict = {}, {}, {}
    # 记录25个供应点的初始坐标
    position = []
    # 对数据进行分组 
    for i in range(point_nums-1):
        people_dict[i] = data.comm_people_nums[volume_nums*i : volume_nums*(i+1)]
        x_dict[i] = data.comm_x_axis[volume_nums*i : volume_nums*(i+1)]
        y_dict[i] = data.comm_y_axis[volume_nums*i : volume_nums*(i+1)]
    people_dict[point_nums-1] = data.comm_index[volume_nums*(point_nums-1):]
    x_dict[point_nums-1] = data.comm_x_axis[volume_nums*(point_nums-1):]
    y_dict[point_nums-1] = data.comm_y_axis[volume_nums*(point_nums-1):]

    p_list = []
    for i in range(point_nums):
        p = single_point(people_dict[i], x_dict[i], y_dict[i])
        p_list.append(p)

    people_all_list = data.comm_people_nums
    xall_list = data.comm_x_axis
    yall_list = data.comm_y_axis
    count_p_list = []
    # 进行迭代训练
    ans_count, ans_plist, ans_people = {}, {} , {}
    for e in range(EPOCH):
        for i in range(point_nums):
            cost = trans_cost(p_list[i][0], p_list[i][1], people_all_list, xall_list, yall_list)
            cost_ = cost[np.newaxis, :]
            if i == 0:
                # 计算运送到每个点的损失
                cost_array = cost_
            else:
                cost_array = np.concatenate((cost_array, cost_), axis=0)
        
        # 重新划分组
        people_dict = dict([(k, []) for k in range(volume_nums)])
        x_dict = dict([(k, []) for k in range(volume_nums)])
        y_dict = dict([(k, []) for k in range(volume_nums)])
        comm_count = dict([(k, []) for k in range(volume_nums)])
        for i in range(data.comm_nums):
            index = np.argmin(cost_array[:, i])
            people_dict[index].append(people_all_list[i])
            x_dict[index].append(xall_list[i])
            y_dict[index].append(yall_list[i])
            comm_count[index].append(i)

        p_list = []
        for i in range(point_nums):
            p = single_point(people_dict[i], x_dict[i], y_dict[i])
            p_list.append(p)
        
        count_p_list.append(p_list)
        if e > 3:
            for i in range(volume_nums):
                if count_p_list[-1][i][0] and count_p_list[-2][i][0] :
                    loss = abs(count_p_list[-1][i][0]- count_p_list[-2][i][0])
                    if  abs(count_p_list[-1][i][0]- count_p_list[-2][i][0])< 0.01:
                        ans_count = comm_count
                        ans_people = people_dict
                        ans_plist = count_p_list[-1]
                        break
            if loss < 0.01:
                break
            if e % 100 == 0:
                print("Epoch: [%d/%d], loss : %.4f, comm_count[0]: %d" %
                                (e, EPOCH, loss, len(comm_count[0])))
    point_people_count, point_nums_count = [0] * point_nums, [0] * point_nums
    for i in range(point_nums):
        point_nums_count[i] = len(ans_count[i])
        point_people_count[i] = sum(ans_people[i])
    print("每个投放点可以覆盖多少个小区", point_nums_count)
    print("每个投放点的坐标", ans_plist)
    print("ans_people:", point_people_count)

    draw_plt(ans_plist, data.comm_x_axis, data.comm_y_axis, data.comm_loca_index, plt_save)
    min_index_list = [] # 距离最近的小区（所属区域）
    point_radius = [] # 选址半径 距离最远的小区
    comm_dst = {
        0:'宽城区',
        1:'二道区',
        2:'朝阳区',
        3:'绿园区',
        4:'南关区',
        5:'经开区',
        6:'长春新区(高新)',
        7:'净月区',
        8:'汽开区'
        }
    label = []
    for i in range(9):
        label = label + [i] * data.comm_loca_index[i]
        
    # 计算所属区域
    for i in range(point_nums):
        x, y = ans_plist[i][0], ans_plist[i][1]
        dis = center_distence(x, y, data.comm_x_axis, data.comm_y_axis)
        min_dis_index = dis.index(min(dis))
        min_name = comm_dst[label[min_dis_index]]
        point_radius.append(min(dis))
        min_index_list.append(min_name)
    ans_people_count = []
    ans_comm_count = []
    for i in range(point_nums):
        ans_people_count.append(sum(ans_people[i]))
        ans_comm_count.append(sum(ans_count[i]))
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

    excel_data = []
    excel_data.append(ans_plist)
    excel_data.append(min_index_list)
    excel_data.append(point_radius)
    excel_data.append(ans_comm_count)
    excel_data.append(ans_people_count)
    save_file = str(point_nums) + '_ans.xlsx'
    xw_toExcel(excel_data, save_file)
        










