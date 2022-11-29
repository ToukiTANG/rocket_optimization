import geatpy as ea
import numpy as np

from .atmospheric_model import G0
from .runge_kutta import RK

n_y_max = G0
w_v = 1
w_h = 1
w_q = 1
w_theta = 1
w_n_y = 1


class Problem(ea.Problem):
    def __init__(self, constraint):
        # 包含约束与载荷、半径
        self.v_con = constraint.v_con
        self.h_con = constraint.h_con
        self.q_max = constraint.q_max
        self.theta_last = constraint.theta_last
        self.load_m = constraint.load_m
        self.radius = constraint.radius
        # 燃料比冲数组和连续变量的上下界
        self.var_set = np.array(constraint.isp_arr)
        self.lb = constraint.lb
        self.ub = constraint.ub

        name = "ProblemClss"
        M = 1  # 目标维数
        maxormins = [1]  # 目标最大最小化标记，1：min；-1：max
        Dim = 13  # 决策变量维数
        varTypes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]  # 决策变量类型。0：连续；1：离散
        # [m_1-3;p_1-3;i_sp1-3;alpha_m,a,d_phi1-2]
        for i in range(3):
            self.lb.append(0)
            self.ub.append(len(constraint.isp_arr) - 1)
        # lb = [15000, 6000, 3200, 650000, 269000, 140000, 2, 0.1, 0.2, 0.2, 0, 0, 0]  # 决策变量下界
        # ub = [20000, 7000, 3700, 700000, 280000, 147000, 5, 0.2, 0.4, 0.4, 6, 6, 6]  # 决策变量上界
        self.L = np.sum(self.lb[0:3])
        self.U = np.sum(self.ub[0:3])
        lbin = [1] * Dim  # 决策变量上边界(为“1”表示有能取到边界)
        ubin = [1] * Dim  # 决策变量下边界
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, self.lb, self.ub, lbin, ubin)  # 调用父类构造方法完成初始化

    def aimFunc(self, pop):  # pop为种群
        Vars = pop.Phen
        pop.ObjV = []
        for i in range(Vars.shape[0]):
            var_com = Vars[i, :]

            m1 = var_com[0]
            m2 = var_com[1]
            m3 = var_com[2]
            p1 = var_com[3]
            p2 = var_com[4]
            p3 = var_com[5]

            # i_sp1 = i_sp_arr[(var_com[:, [6]])]
            # i_sp2 = i_sp_arr[(var_com[:, [7]])]
            # i_sp3 = i_sp_arr[(var_com[:, [8]])]

            i_sp1 = self.var_set[(var_com[10]).astype(np.int32)]
            i_sp2 = self.var_set[(var_com[11]).astype(np.int32)]
            i_sp3 = self.var_set[(var_com[12]).astype(np.int32)]

            alpha_m = var_com[6]
            a = var_com[7]
            d_phi1 = var_com[8]
            d_phi2 = var_com[9]

            v = 0.0001
            theta = 90
            x = 0
            y = 0
            m = m1 + m2 + m3 + self.load_m  # 载荷
            s_m = np.pi * self.radius ** 2
            # print("i:", i)
            re_list = RK([m1, m2, m3], [p1, p2, p3], [i_sp1, i_sp2, i_sp3], v, theta, x, y, m, s_m, alpha_m, a, d_phi1,
                         d_phi2,
                         time_step=0.1)
            t_array, v_array, theta_array, x_array, h_array, m_array, q_array, n_y_array = re_list
            m = ((m1 + m2 + m3) - self.L) / (self.U - self.L)  # 质量归一化
            result = m + w_v * (np.max([0, self.normalization(np.abs(v_array[-1] - self.v_con))]) ** 2) + w_h * (
                    np.max([0, self.normalization(np.abs(h_array[-1] - self.h_con))]) ** 2) + w_q * (
                             np.min([0, self.q_max - np.max(q_array)]) ** 2) + w_theta * (
                             np.max([0, self.normalization(np.abs(theta_array[-1] - self.theta_last))]) ** 2)
            pop.ObjV.append(result)
        pop.ObjV = np.array(pop.ObjV)
        pop.ObjV = pop.ObjV.reshape((Vars.shape[0], 1))

    @staticmethod
    def normalization(x):
        return 1 / (1 + np.exp(-x))
