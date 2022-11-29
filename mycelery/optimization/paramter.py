class Constraint:
    def __init__(self, v_con, h_con, q_max, theta_last, load_m, radius, isp_arr, lb_arr, ub_arr):
        self.v_con = v_con
        self.h_con = h_con
        self.q_max = q_max
        self.theta_last = theta_last
        self.load_m = load_m
        self.radius = radius
        self.isp_arr = isp_arr
        self.lb = lb_arr
        self.ub = ub_arr
