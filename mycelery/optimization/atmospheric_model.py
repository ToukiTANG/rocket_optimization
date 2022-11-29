import numpy as np

# 标准重力加速度
G0 = 9.80665

# 引力常数
fm = 3.986005 * np.power(10, 24)

# 地球半径
R = 6378137

# 海平面温度
T_sl = 288.15

# 海平面声速
A_sl = 340.294

# 海平面压力(N/m^2,注释为kg/m^2)
P_sl = 101325
# P_sl=10332.3

# 海平面密度
Rho_sl = 1.225


# 计算重力加速度
def get_g(r):
    if r < R:
        raise ValueError("------------高度异常--------------")
    else:
        return -fm / (r ** 2)


# 计算温度

def get_T(h):
    H = h / (1 + h / R) / 1000
    if h < 0:
        raise ValueError("------------高度异常--------------")
    elif h <= 11019.1:
        W = 1 - H / 44.3308
        T = 288.15 * W
        return T
    elif h <= 20063.1:
        W = np.exp((14.9647 - H) / 6.3416)
        T = 216.650
        return T
    elif h <= 32161.9:
        W = 1 + (H - 24.9021) / 221.552
        T = 221.552 * W
        return T
    elif h <= 47350.1:
        W = 1 + (H - 39.7499) / 89.4107
        T = 250.350 * W
        return T
    elif h <= 51412.5:
        W = np.exp((48.6252 - H) / 7.9223)
        T = 270.650
        return T
    elif h <= 71802.0:
        W = 1 - (H - 59.4390) / 88.2218
        T = 247.021 * W
        return T
    elif h <= 86000.0:
        W = 1 - (H - 78.0303) / 100.2950
        T = 200.590 * W
        return T
    elif h < 91000.0:
        W = np.exp((87.2848 - H) / 5.4700)
        T = 186.87
        return T
    else:
        H = R * 91000 / (R + 91000) / 1000
        W = np.exp((87.2848 - H) / 5.47)
        T = 186.87
        return T


# 计算压强

def get_P(h):
    H = h / (1 + h / R) / 1000
    if h < 0:
        raise ValueError("------------高度异常--------------")
    elif h <= 11019.1:
        W = 1 - H / 44.3308
        P = np.power(W, 5.2559) * P_sl
        return P
    elif h <= 20063.1:
        W = np.exp((14.9647 - H) / 6.3416)
        P = W * 0.11953 * P_sl
        return P
    elif h <= 32161.9:
        W = 1 + (H - 24.9021) / 221.552
        P = 0.025158 * np.power(W, -34.1629) * P_sl
        return P
    elif h <= 47350.1:
        W = 1 + (H - 39.7499) / 89.4107
        P = 2.8338 * 0.001 * np.power(W, -12.2011) * P_sl
        return P
    elif h <= 51412.5:
        W = np.exp((48.6252 - H) / 7.9223)
        P = 8.9155 * 0.0001 * W * P_sl
        return P
    elif h <= 71802.0:
        W = 1 - (H - 59.4390) / 88.2218
        P = 2.1671 * 0.0001 * np.power(W, 12.2011) * P_sl
        return P
    elif h <= 86000.0:
        W = 1 - (H - 78.0303) / 100.2950
        P = 1.2274 * 0.00001 * np.power(W, 17.0816) * P_sl
        return P
    elif h < 91000.0:
        W = np.exp((87.2848 - H) / 5.4700)
        P = (2.2730 + 1.042 * 0.001 * H) * 0.000001 * W * P_sl
        return P
    else:
        H = R * 91000 / (R + 91000) / 1000
        W = np.exp((87.2848 - H) / 5.47)
        P = (2.2730 + 1.042 * 0.001 * H) * 0.000001 * W * P_sl
        return P


# 计算密度
def get_Rho(h):
    H = h / (1 + h / R) / 1000
    if h < 0:
        raise ValueError("------------高度异常--------------")
    elif h <= 11019.1:
        W = 1 - H / 44.3308
        RHO = np.power(W, 4.2559) * Rho_sl
        return RHO
    elif h <= 20063.1:
        W = np.exp((14.9647 - H) / 6.3416)
        RHO = W * 0.15898 * Rho_sl
        return RHO
    elif h <= 32161.9:
        W = 1 + (H - 24.9021) / 221.552
        RHO = 0.032722 * np.power(W, -35.1629) * Rho_sl
        return RHO
    elif h <= 47350.1:
        W = 1 + (H - 39.7499) / 89.4107
        RHO = 3.2618 * 0.001 * np.power(W, -13.2011) * Rho_sl
        return RHO
    elif h <= 51412.5:
        W = np.exp((48.6252 - H) / 7.9223)
        RHO = 9.4920 * 0.0001 * W * Rho_sl
        return RHO
    elif h <= 71802.0:
        W = 1 - (H - 59.4390) / 88.2218
        RHO = 2.5280 * 0.0001 * np.power(W, 11.2011) * Rho_sl
        return RHO
    elif h <= 86000.0:
        W = 1 - (H - 78.0303) / 100.2950
        RHO = 1.7632 * 0.00001 * np.power(W, 16.0816) * Rho_sl
        return RHO
    elif h < 91000.0:
        W = np.exp((87.2848 - H) / 5.4700)
        RHO = 3.6411 * 0.000001 * W * Rho_sl
        return RHO
    else:
        H = R * 91000 / (R + 91000) / 1000
        W = np.exp((87.2848 - H) / 5.47)
        RHO = 3.6411 * 0.000001 * W * Rho_sl
        return RHO


# 计算声速
def get_sound_speed(T):
    AS = 20.0468 * np.sqrt(T)
    return AS
