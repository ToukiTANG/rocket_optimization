import geatpy as ea
import numpy as np

from myapp import utils
from myapp.models import OptimizedState, OptimizedResult
from myapp.models import Task, InitialState, ConstParam, ParamScope, GA
from mycelery.main import app
from . import paramter
from . import problem
from .runge_kutta import RK


@app.task
def optimization_executor(task_id, initial_state_id, const_param_id, param_scope_id, ga_param_id):
    task = Task.objects.get(id=task_id)
    initialParam = InitialState.objects.get(id=initial_state_id)
    constParam = ConstParam.objects.get(id=const_param_id)
    paramScope = ParamScope.objects.get(id=param_scope_id)
    gaParam = GA.objects.get(id=ga_param_id)
    # 优化常量
    v_con = float(constParam.v_con)
    h_con = float(constParam.h_con)
    q_max = float(constParam.q_max)
    theta_last = float(constParam.theta_last)
    load_m = float(constParam.load_m)
    radius = float(constParam.radius)
    # 上下界数组
    lb = []
    ub = []
    # 比冲数组
    isp_scope = utils.str2int_arr(paramScope.isp_scope)

    m_l_scope = utils.str2int_arr(paramScope.m_l_scope)
    lb.extend(m_l_scope)
    m_u_scope = utils.str2int_arr(paramScope.m_u_scope)
    ub.extend(m_u_scope)
    p_l_scope = utils.str2int_arr(paramScope.p_l_scope)
    lb.extend(p_l_scope)
    p_u_scope = utils.str2int_arr(paramScope.p_u_scope)
    ub.extend(p_u_scope)
    alpha_scope = utils.str2float_arr(paramScope.alpha_m_scope)
    lb.append(alpha_scope[0])
    ub.append(alpha_scope[1])
    a_scope = utils.str2float_arr(paramScope.a_scope)
    lb.append(a_scope[0])
    ub.append(a_scope[1])
    dphi_l_scope = utils.str2float_arr(paramScope.dphi_l_scope)
    lb.extend(dphi_l_scope)
    dphi_u_scope = utils.str2float_arr(paramScope.dphi_u_scope)
    ub.extend(dphi_u_scope)
    print(lb)
    print(ub)
    param = paramter.Constraint(v_con=v_con, h_con=h_con, q_max=q_max, theta_last=theta_last, load_m=load_m,
                                radius=radius, isp_arr=isp_scope, lb_arr=lb, ub_arr=ub)
    # 构建问题
    pro = problem.Problem(constraint=param)
    encoding = "RI"
    NIND = gaParam.nind
    Field = ea.crtfld(encoding, pro.varTypes, pro.ranges, pro.borders)
    population = ea.Population(encoding, Field, NIND)

    myAlgorithm = ea.soea_DE_best_1_L_templet(pro, population)
    myAlgorithm.MAXGEN = gaParam.maxgen
    myAlgorithm.mutOper.F = float(gaParam.f)
    myAlgorithm.recOper.XOVR = float(gaParam.xovr)
    myAlgorithm.logTras = 1
    myAlgorithm.verbose = True
    myAlgorithm.drawing = 0
    [BestIndi, population] = myAlgorithm.run()
    best_record = myAlgorithm.trace['f_best']

    # 存储优化后状态
    chrom = BestIndi.Chrom[0]
    m_arr_str = utils.arr2str([round(chrom[0], 3), round(chrom[1], 3), round(chrom[2], 3)])
    p_arr_str = utils.arr2str([round(chrom[3], 3), round(chrom[4], 3), round(chrom[5], 3)])
    isp_arr_str = utils.arr2str([isp_scope[(chrom[10]).astype(np.int32)], isp_scope[(chrom[11]).astype(np.int32)],
                                 isp_scope[(chrom[12]).astype(np.int32)]])
    alpha_m = round(chrom[6], 3)
    a = round(chrom[7], 3)
    dphi_arr_str = utils.arr2str([round(chrom[8], 3), round(chrom[9], 3)])
    OptimizedState.objects.create(task_id=task.id, m_arr=m_arr_str, p_arr=p_arr_str, isp_arr=isp_arr_str,
                                  alpha_m=alpha_m, a=a, dphi_arr=dphi_arr_str)
    task.state = True
    task.save()

    # 计算优化前曲线
    m_arr_init = utils.str2int_arr(initialParam.m_arr)
    p_arr_init = utils.str2int_arr(initialParam.p_arr)
    isp_arr_init = utils.str2int_arr(initialParam.isp_arr)
    dphi_arr_init = utils.str2float_arr(initialParam.dphi_arr)
    a_init = float(initialParam.a)
    alpha_m_init = float(initialParam.alpha_m)
    t_array, v_array, theta_array, x_array, h_array, m_array, q_array, n_y_array = RK(m_arr=m_arr_init,
                                                                                      p_arr=p_arr_init,
                                                                                      i_sp_arr=isp_arr_init,
                                                                                      v=0.0000001,
                                                                                      theta=90, x=0, y=0,
                                                                                      m=sum(m_arr_init) + load_m,
                                                                                      s_m=np.pi * radius ** 2,
                                                                                      alpha_m=alpha_m_init, a=a_init,
                                                                                      d_phi1=dphi_arr_init[0],
                                                                                      d_phi2=dphi_arr_init[1],
                                                                                      time_step=0.1)
    print(len(t_array), len(v_array), len(theta_array))
    # 储存优化前的结果状态
    OptimizedResult.objects.create(task_id=task_id, optimized=False, t_arr=utils.arr2str(t_array),
                                   v_arr=utils.arr2str(v_array), phi_arr=utils.arr2str(theta_array),
                                   h_arr=utils.arr2str(h_array), q_arr=utils.arr2str(q_array))
    # 计算优化后曲线
    t_array, v_array, theta_array, x_array, h_array, m_array, q_array, n_y_array = RK(
        m_arr=utils.str2float_arr(m_arr_str), p_arr=utils.str2float_arr(p_arr_str),
        i_sp_arr=utils.str2int_arr(isp_arr_str), v=0.0000001, theta=90, x=0, y=0,
        m=sum(utils.str2float_arr(m_arr_str)) + load_m, s_m=np.pi * radius ** 2, alpha_m=alpha_m, a=a,
        d_phi1=utils.str2float_arr(dphi_arr_str)[0], d_phi2=utils.str2float_arr(dphi_arr_str)[1], time_step=0.1)
    OptimizedResult.objects.create(task_id=task_id, optimized=True, t_arr=utils.arr2str(t_array),
                                   v_arr=utils.arr2str(v_array), phi_arr=utils.arr2str(theta_array),
                                   h_arr=utils.arr2str(h_array), q_arr=utils.arr2str(q_array),
                                   record_arr=utils.arr2str(best_record))
    return "ok"
