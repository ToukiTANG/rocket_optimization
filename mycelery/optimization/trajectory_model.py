import numpy as np

from . import atmospheric_model as am


def get_c_d(Ma):
    if Ma < 0:
        raise ValueError("------------声速异常--------------")
    elif Ma <= 0.8:
        return 0.29
    elif Ma <= 1.07:
        return Ma - 0.51
    else:
        return 0.091 + 1 / 2 * Ma


def get_c_alpha(Ma):
    if Ma < 0:
        raise ValueError("------------声速异常--------------")
    elif Ma <= 0.25:
        return 2.8
    elif Ma <= 1.1:
        return 2.8 + 0.447 * (Ma - 0.25)
    elif Ma <= 1.6:
        return 3.18 - 0.66 * (Ma - 1.1)
    elif Ma <= 3.6:
        return 2.85 + 0.350 * (Ma - 1.6)
    else:
        return 3.55


def func_v(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi):
    r = np.sqrt(x ** 2 + (y + am.R) ** 2)
    h = r - am.R
    Ma = v / am.get_sound_speed(am.get_T(h))
    q = am.get_Rho(h) * 0.5 * v ** 2
    c_d = get_c_d(Ma)
    g = am.get_g(r)
    return (p - c_d * q * s_m + m * g * np.sin(np.deg2rad(theta)) * (y + am.R) / r + m * g * np.cos(
        np.deg2rad(theta)) * x / r) / m


def func_theta(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi):
    r = np.sqrt(x ** 2 + (y + am.R) ** 2)
    h = r - am.R
    Ma = v / am.get_sound_speed(am.get_T(h))
    q = am.get_Rho(h) * 0.5 * v ** 2
    c_alpha = get_c_alpha(Ma)
    g = am.get_g(r)
    return (p + c_alpha * q * s_m) * alpha / (v * m) + (g * np.cos(np.deg2rad(theta)) * ((y + am.R) / r)) / v - (
            g * (x / r) * np.sin(theta) / v)


def func_theta_linear(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi):
    return -d_phi


def func_y(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi):
    return v * np.sin(np.deg2rad(theta))


def func_x(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi):
    return v * np.cos(np.deg2rad(theta))


def func_m(v, theta, x, y, m, p, i_sp, s_m, alpha, d_phi):
    return -p / i_sp
