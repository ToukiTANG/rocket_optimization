import json

import jsonpickle
from django.http import HttpResponse

from mycelery.optimization.tasks import optimization_executor
from . import utils
from .models import Task, InitialState, ConstParam, ParamScope, GA, OptimizedState, OptimizedResult


def task_list(request):
    task = Task.objects.all().order_by('-create_time')
    task = utils.serialize_object(task)
    return HttpResponse(content=task, status=200)


def task_detail(request):
    task_id = request.GET['id']
    task = Task.objects.get(id=task_id)
    ga = GA.objects.get(task_id=task_id)

    optimizedState = OptimizedState.objects.get(task_id=task_id)
    optimizedState.m_arr = utils.str2float_arr(optimizedState.m_arr)
    optimizedState.p_arr = utils.str2float_arr(optimizedState.p_arr)
    optimizedState.isp_arr = utils.str2int_arr(optimizedState.isp_arr)
    optimizedState.dphi_arr = utils.str2float_arr(optimizedState.dphi_arr)

    initialState = InitialState.objects.get(task_id=task_id)
    initialState.m_arr = utils.str2int_arr(initialState.m_arr)
    initialState.p_arr = utils.str2int_arr(initialState.p_arr)
    initialState.isp_arr = utils.str2int_arr(initialState.isp_arr)
    initialState.dphi_arr = utils.str2float_arr(initialState.dphi_arr)

    constParam = ConstParam.objects.get(task_id=task_id)
    paramScope = ParamScope.objects.get(task_id=task_id)
    paramScope.m_l_scope = utils.str2int_arr(paramScope.m_l_scope)
    paramScope.m_u_scope = utils.str2int_arr(paramScope.m_u_scope)
    paramScope.p_l_scope = utils.str2int_arr(paramScope.p_l_scope)
    paramScope.p_u_scope = utils.str2int_arr(paramScope.p_u_scope)
    paramScope.isp_scope = utils.str2int_arr(paramScope.isp_scope)
    paramScope.dphi_l_scope = utils.str2float_arr(paramScope.dphi_l_scope)
    paramScope.dphi_u_scope = utils.str2float_arr(paramScope.dphi_u_scope)
    paramScope.alpha_m_scope = utils.str2float_arr(paramScope.alpha_m_scope)
    paramScope.a_scope = utils.str2float_arr(paramScope.a_scope)

    result = jsonpickle.encode(
        {'task': task, 'ga': ga, 'initialState': initialState, 'constParam': constParam, 'paramScope': paramScope,
         'optimizedState': optimizedState},
        unpicklable=False, use_decimal=True)
    return HttpResponse(content=result, status=200)


def task_new(request):
    # 拿到请求参数
    request_body = request.body
    body_json = bytes.decode(request_body)
    body_dict = json.loads(body_json)

    # 存储任务信息
    task = Task.objects.create(description=utils.get_task(body_dict)['description'])

    # 存储初始状态
    initial_state = utils.get_initial_state(body_dict)
    m_arr_str = initial_state['m_arr']
    p_arr_str = initial_state['p_arr']
    isp_arr_str = initial_state['isp_arr']
    alpha_m = float(initial_state['alpha_m'])
    a = float(initial_state['a'])
    dphi_arr_str = initial_state['d_phi']
    initialState = InitialState.objects.create(task_id=task.id, m_arr=m_arr_str, p_arr=p_arr_str, isp_arr=isp_arr_str,
                                               alpha_m=alpha_m,
                                               a=a, dphi_arr=dphi_arr_str)

    # 储存优化常量与约束
    const_param = utils.get_const_param(body_dict)
    load_m = const_param['load_m']
    radius = float(const_param['radius'])
    v_con = const_param['v_con']
    h_con = const_param['h_con']
    q_max = const_param['q_max']
    theta_last = const_param['theta_last']
    constParam = ConstParam.objects.create(task_id=task.id, load_m=load_m, radius=radius, v_con=v_con, h_con=h_con,
                                           q_max=q_max,
                                           theta_last=theta_last)

    # 储存参数范围约束
    param_scope = utils.get_param_scope(body_dict)
    m_l_scope = param_scope['m_l_scope']
    m_u_scope = param_scope['m_u_scope']
    p_l_scope = param_scope['p_l_scope']
    p_u_scope = param_scope['p_u_scope']
    isp_scope = param_scope['isp_scope']
    dphi_l_scope = param_scope['dphi_l_scope']
    dphi_u_scope = param_scope['dphi_u_scope']
    alpha_m_scope = param_scope['alpha_m_scope']
    a_scope = param_scope['a_scope']
    paramScope = ParamScope.objects.create(task_id=task.id, m_l_scope=m_l_scope, m_u_scope=m_u_scope,
                                           p_l_scope=p_l_scope,
                                           p_u_scope=p_u_scope, isp_scope=isp_scope, dphi_l_scope=dphi_l_scope,
                                           dphi_u_scope=dphi_u_scope, alpha_m_scope=alpha_m_scope, a_scope=a_scope)

    # 储存GA参数
    ga = utils.get_GA(body_dict)
    nind = ga['nind']
    maxgen = ga['maxgen']
    f = float(ga['f'])
    xovr = float(ga['xovr'])
    gaParam = GA.objects.create(task_id=task.id, nind=nind, maxgen=maxgen, f=f, xovr=xovr)
    # 异步执行
    optimization_executor.delay(task.id, initialState.id, constParam.id, paramScope.id, gaParam.id)
    return HttpResponse(content="success", status=200)


def task_visualization(request):
    task_id = request.GET['id']
    unOptimizedResult = OptimizedResult.objects.get(task_id=task_id, optimized=False)
    optimizedResult = OptimizedResult.objects.get(task_id=task_id, optimized=True)

    unOptimizedResult.t_arr = utils.str2float_arr(unOptimizedResult.t_arr, pre=1)
    unOptimizedResult.v_arr = utils.str2float_arr(unOptimizedResult.v_arr)
    unOptimizedResult.phi_arr = utils.str2float_arr(unOptimizedResult.phi_arr)
    unOptimizedResult.h_arr = utils.str2float_arr(unOptimizedResult.h_arr)
    unOptimizedResult.q_arr = utils.str2float_arr(unOptimizedResult.q_arr)

    optimizedResult.t_arr = utils.str2float_arr(optimizedResult.t_arr, pre=1)
    optimizedResult.v_arr = utils.str2float_arr(optimizedResult.v_arr)
    optimizedResult.phi_arr = utils.str2float_arr(optimizedResult.phi_arr)
    optimizedResult.h_arr = utils.str2float_arr(optimizedResult.h_arr)
    optimizedResult.q_arr = utils.str2float_arr(optimizedResult.q_arr)
    optimizedResult.record_arr = utils.str2float_arr(optimizedResult.record_arr, pre=6)

    result = jsonpickle.encode({'unOptimizedResult': unOptimizedResult, 'optimizedResult': optimizedResult},
                               unpicklable=False)
    return HttpResponse(content=result, status=200)
