import pandas as pd
import numpy as np
import load_data

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

# 计算运输费用
def trans_cost(x, y, volume_list, x_list, y_list):
	D = center_distence(x, y, x_list, y_list)
	return np.multiply(volume_list, D)

if __name__ == '__main__':
    abs_path = "/Users/candy/Documents/资源/研究生工作/浙江理工/数学建模/code/data/"
    path = "./data/"
    sheet = "excel3.xlsx"
    data = load_data.dataset(
        path=abs_path,
        sheet=sheet
    )
    
