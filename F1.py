
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
# 线性平移预处理，确保数据级比在可容覆盖范围
def greyModelPreprocess(dataVec):
    "Set linear-bias c for dataVec"
    import numpy as np
    from scipy import io, integrate, linalg, signal
    from scipy.sparse.linalg import eigs
    from scipy.integrate import odeint

    c = 0
    x0 = np.array(dataVec, float)
    n = x0.shape[0]
    L = np.exp(-2/(n+1))
    R = np.exp(2/(n+2))
    xmax = x0.max()
    xmin = x0.min()
    if (xmin < 1):
        x0 += (1-xmin)
        c += (1-xmin)
    xmax = x0.max()
    xmin = x0.min()
    lambda_ = x0[0:-1] / x0[1:]  # 计算级比
    lambda_max = lambda_.max()
    lambda_min = lambda_.min()
    while (lambda_max > R or lambda_min < L):
        x0 += xmin
        c += xmin
        xmax = x0.max()
        xmin = x0.min()
        lambda_ = x0[0:-1] / x0[1:]
        lambda_max = lambda_.max()
        lambda_min = lambda_.min()
    return c

# 灰色预测模型
def greyModel(dataVec, predictLen):
    "Grey Model for exponential prediction"
    # dataVec = [1, 2, 3, 4, 5, 6]
    # predictLen = 5
    import numpy as np
    from scipy import io, integrate, linalg, signal
    from scipy.sparse.linalg import eigs
    from scipy.integrate import odeint

    x0 = np.array(dataVec, float)
    n = x0.shape[0]
    x1 = np.cumsum(x0)
    B = np.array([-0.5 * (x1[0:-1] + x1[1:]), np.ones(n-1)]).T
    Y = x0[1:]
    u = linalg.lstsq(B, Y)[0]

    def diffEqu(y, t, a, b):
        return np.array(-a * y + b)

    t = np.arange(n + predictLen)
    sol = odeint(diffEqu, x0[0], t, args=(u[0], u[1]))
    sol = sol.squeeze()
    res = np.hstack((x0[0], np.diff(sol)))
    return res

import scipy.stats as stats
def cox_stuart(list_c,debug=False):
	lst=list_c.copy()
	raw_len=len(lst)
	if raw_len%2==1:
		del lst[int((raw_len-1)/2)]    # 删除中位数
	c=int(len(lst)/2)
	n_pos=n_neg=0
	for i in range(c):
		diff=lst[i+c]-lst[i]
		if diff>0:
			n_pos+=1
		elif diff<0:
			n_neg+=1
		else:
			continue
	num=n_pos+n_neg
	k=min(n_pos,n_neg)           #  双边检验
	print("k: ",k)
	print("num:",num)
	p_value=2*stats.binom.cdf(k,num,0.5)  #  二项分布
	if debug:
		print('fall:%i, rise:%i, p-value:%f'%(n_neg, n_pos, p_value))
	if n_pos>n_neg and p_value<0.05:   #  双边检验
		return 'increasing'
	elif n_neg>n_pos and p_value<0.05:  #  双边检验
		return 'decreasing'
	else:
		return 'no trend'
	if n_pos>n_neg :   #  双边检验
		return 'increasing'
	elif n_neg>n_pos :  #  双边检验
		return 'decreasing'
	else:
		return 'no trend'

# 输入数据
df1 = pd.read_excel("data/excel_from_bi.xlsx",'新增预测')
df1 = df1.values
df1 = np.delete(df1,0,axis=1)
df_T = pd.read_excel("data/excel_from_bi.xlsx",'新增实际')
df_T = df_T.values
df_T = np.delete(df_T,0,axis=1)
# 实际疫情发展情况
INDEX = 8
y = df_T.T[INDEX,:].tolist()
res = cox_stuart(y, True)
print(res)

# for i in range(9):
#     x = df1.T[i,:]
#     print(x)
#     y = df_T.T[i,:] 
#     print(y)
#     # x = np.array([-18, 0.34, 4.68, 8.49, 29.84, 50.21, 77.65, 109.36])
#     c = greyModelPreprocess(x)
#     x_hat = greyModel(x+c, 18)-c

#     # 画图
#     t1 = range(x.size)
#     t2 = range(x_hat.size)
#     # plt.plot(t1, x, color='r', linestyle="-", marker='*', label='3.26 发放蔬菜包前')
#     plt.plot(range(13,32),y,color='black',linestyle="-",marker='+',label ="物资投放后")
#     # plt.plot(t2, x_hat, color='b', linestyle="--", marker='.', label="Predict")
#     plt.legend(loc='upper right')
#     plt.xlabel('天数')
#     plt.ylabel('新增人数')
#     title_str = ['长春新区', '净月区', '绿园区', '朝阳区', '经开区', '宽城区', '南关区', '汽开区', '二道区']
#     plt.title(title_str[i])
#     plt.show()
