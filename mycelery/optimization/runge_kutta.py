import numpy as np

from . import atmospheric_model as am
from . import trajectory_model as tm


def RK(m_arr, p_arr, i_sp_arr, v, theta, x, y, m, s_m, alpha_m, a, d_phi1, d_phi2, time_step):
    m1, m2, m3 = m_arr
    p1, p2, p3 = p_arr
    i_sp1, i_sp2, i_sp3 = i_sp_arr
    d_phi = 0

    t_array = []
    v_array = []
    theta_array = []
    x_array = []
    h_array = []
    m_array = []
    q_array = []
    n_y_array = []

    h = time_step
    t = 0

    t_array.append(t)
    v_array.append(v)
    theta_array.append(theta)
    x_array.append(x)
    h_array.append(0)
    m_array.append(m)
    q_array.append(0)
    n_y_array.append(0)

    t1 = np.sqrt(40 * m * am.G0 / p1 / (1 - m * am.G0 / p1))
    t_m = m1 / (p1 / i_sp1) + m2 / (p2 / i_sp2) + m3 / (p3 / i_sp3)
    while t <= t_m:
        t += h

        if t <= t1:
            alpha = 0
        else:
            alpha = 4 * alpha_m * np.exp(a * (t1 - t)) * (np.exp(a * (t1 - t)) - 1)
        if t <= m1 / (p1 / i_sp1):
            p = p1
            i_sp = i_sp1
        elif t <= m1 / (p1 / i_sp1) + m2 / (p2 / i_sp2):
            p = p2
            i_sp = i_sp2
        else:
            p = p3
            i_sp = i_sp3

        try:
            v_k1 = tm.func_v(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi)
            if t <= m1 / (p1 / i_sp1):
                theta_k1 = tm.func_theta(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi)
            elif t <= m1 / (p1 / i_sp1) + m2 / (p2 / i_sp2):
                d_phi = d_phi1
                theta_k1 = tm.func_theta_linear(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi)
            else:
                d_phi = d_phi2
                theta_k1 = tm.func_theta_linear(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi)
            x_k1 = tm.func_x(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi)
            y_k1 = tm.func_y(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi)
            m_k1 = tm.func_m(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi)

            v_k2 = tm.func_v(v + v_k1 * h / 2, theta + theta_k1 * h / 2, x + x_k1 * h / 2, y + y_k1 * h / 2,
                             m + m_k1 * h / 2, p, i_sp, s_m, alpha, d_phi)
            if t <= m1 / (p1 / i_sp1):
                theta_k2 = tm.func_theta(v + v_k1 * h / 2, theta + theta_k1 * h / 2, x + x_k1 * h / 2, y + y_k1 * h / 2,
                                         m + m_k1 * h / 2, p, i_sp, s_m, alpha, d_phi)
            else:
                theta_k2 = tm.func_theta_linear(v + v_k1 * h / 2, theta + theta_k1 * h / 2, x + x_k1 * h / 2,
                                                y + y_k1 * h / 2,
                                                m + m_k1 * h / 2, p, i_sp, s_m, alpha, d_phi)
            x_k2 = tm.func_x(v + v_k1 * h / 2, theta + theta_k1 * h / 2, x + x_k1 * h / 2, y + y_k1 * h / 2,
                             m + m_k1 * h / 2, p, i_sp, s_m, alpha, d_phi)
            y_k2 = tm.func_y(v + v_k1 * h / 2, theta + theta_k1 * h / 2, x + x_k1 * h / 2, y + y_k1 * h / 2,
                             m + m_k1 * h / 2, p, i_sp, s_m, alpha, d_phi)
            m_k2 = tm.func_m(v + v_k1 * h / 2, theta + theta_k1 * h / 2, x + x_k1 * h / 2, y + y_k1 * h / 2,
                             m + m_k1 * h / 2, p, i_sp, s_m, alpha, d_phi)

            v_k3 = tm.func_v(v + v_k2 * h / 2, theta + theta_k2 * h / 2, x + x_k2 * h / 2, y + y_k2 * h / 2,
                             m + m_k2 * h / 2, p, i_sp, s_m, alpha, d_phi)
            if t <= m1 / (p1 / i_sp1):
                theta_k3 = tm.func_theta(v + v_k2 * h / 2, theta + theta_k2 * h / 2, x + x_k2 * h / 2, y + y_k2 * h / 2,
                                         m + m_k2 * h / 2, p, i_sp, s_m, alpha, d_phi)
            else:
                theta_k3 = tm.func_theta_linear(v + v_k2 * h / 2, theta + theta_k2 * h / 2, x + x_k2 * h / 2,
                                                y + y_k2 * h / 2,
                                                m + m_k2 * h / 2, p, i_sp, s_m, alpha, d_phi)
            x_k3 = tm.func_x(v + v_k2 * h / 2, theta + theta_k2 * h / 2, x + x_k2 * h / 2, y + y_k2 * h / 2,
                             m + m_k2 * h / 2, p, i_sp, s_m, alpha, d_phi)
            y_k3 = tm.func_y(v + v_k2 * h / 2, theta + theta_k2 * h / 2, x + x_k2 * h / 2, y + y_k2 * h / 2,
                             m + m_k2 * h / 2, p, i_sp, s_m, alpha, d_phi)
            m_k3 = tm.func_m(v + v_k2 * h / 2, theta + theta_k2 * h / 2, x + x_k2 * h / 2, y + y_k2 * h / 2,
                             m + m_k2 * h / 2, p, i_sp, s_m, alpha, d_phi)

            v_k4 = tm.func_v(v + v_k3 * h, theta + theta_k3 * h, x + x_k3 * h, y + y_k3 * h, m + m_k3 * h, p, i_sp, s_m,
                             alpha, d_phi)
            if t <= m1 / (p1 / i_sp1):
                theta_k4 = tm.func_theta(v + v_k3 * h, theta + theta_k3 * h, x + x_k3 * h, y + y_k3 * h, m + m_k3 * h,
                                         p,
                                         i_sp,
                                         s_m, alpha, d_phi)
            else:
                theta_k4 = tm.func_theta_linear(v + v_k3 * h, theta + theta_k3 * h, x + x_k3 * h, y + y_k3 * h,
                                                m + m_k3 * h, p,
                                                i_sp,
                                                s_m, alpha, d_phi)
            x_k4 = tm.func_x(v + v_k3 * h, theta + theta_k3 * h, x + x_k3 * h, y + y_k3 * h, m + m_k3 * h, p, i_sp, s_m,
                             alpha, d_phi)
            y_k4 = tm.func_y(v + v_k3 * h, theta + theta_k3 * h, x + x_k3 * h, y + y_k3 * h, m + m_k3 * h, p, i_sp, s_m,
                             alpha, d_phi)
            m_k4 = tm.func_m(v + v_k3 * h, theta + theta_k3 * h, x + x_k3 * h, y + y_k3 * h, m + m_k3 * h, p, i_sp, s_m,
                             alpha, d_phi)

            v = v + h * (v_k1 + 2 * v_k2 + 2 * v_k3 + v_k4) / 6
            theta = theta + h * (theta_k1 + 2 * theta_k2 + 2 * theta_k3 + theta_k4) / 6
            x = x + h * (x_k1 + 2 * x_k2 + 2 * x_k3 + x_k4) / 6
            y = y + h * (y_k1 + 2 * y_k2 + 2 * y_k3 + y_k4) / 6
            # print("v:", v,
            #       "y:",
            #       y, "t:",
            #       t, "theta:",
            #       theta, "alpha:", alpha)
            m = m + h * (m_k1 + 2 * m_k2 + 2 * m_k3 + m_k4) / 6
            r = np.sqrt(x ** 2 + (y + am.R) ** 2)
            high = r - am.R
            rho = am.get_Rho(high)
            q = 0.5 * rho * (v ** 2)
            n_y = (p + tm.get_c_alpha(v / am.get_sound_speed(am.get_T(high)))) * alpha / (m * am.get_g(r))

            # print("t:", t)
            t_array.append(t)
            v_array.append(v)
            theta_array.append(theta)
            x_array.append(x)
            h_array.append(high)
            m_array.append(m)
            q_array.append(q)
            n_y_array.append(n_y)

        except Exception as e:
            print(e)
            t_array.append(t)
            v_array.append(-1)
            theta_array.append(-1)
            x_array.append(-1)
            h_array.append(-1)
            m_array.append(-1)
            q_array.append(-1)
            n_y_array.append(-1)

            break
    re_list = [t_array, v_array, theta_array, x_array, h_array, m_array, q_array, n_y_array]
    return re_list
