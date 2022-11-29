# Create your models here.
from django.db import models
from django.utils import timezone


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField('任务创建时间', default=timezone.now)
    description = models.CharField('任务描述', max_length=100)
    state = models.BooleanField('任务状态', default=False)
    task_name = models.CharField(default='任务', max_length=10)

    def __str__(self):
        return self.task_name


class InitialState(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.IntegerField('任务id', default=0)
    m_arr = models.CharField('质量数组', max_length=255)
    p_arr = models.CharField('推力数组', max_length=255)
    isp_arr = models.CharField('比冲数组', max_length=255)
    alpha_m = models.DecimalField('转弯段攻角绝对值最大值（°）', max_digits=5, decimal_places=3)
    a = models.DecimalField('转弯系数（常数）', max_digits=5, decimal_places=3)
    dphi_arr = models.CharField('俯仰角控制系数数组', max_length=255)
    state_name = models.CharField(default='初始状态', max_length=10)

    def __str__(self):
        return self.state_name


class OptimizedState(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.IntegerField('任务id', default=0)
    m_arr = models.CharField('质量数组', max_length=255)
    p_arr = models.CharField('推力数组', max_length=255)
    isp_arr = models.CharField('比冲数组', max_length=255)
    alpha_m = models.DecimalField('转弯段攻角绝对值最大值（°）', max_digits=5, decimal_places=3)
    a = models.DecimalField('转弯系数（常数）', max_digits=5, decimal_places=3)
    dphi_arr = models.CharField('俯仰角控制系数数组', max_length=255)
    state_name = models.CharField(default='优化状态', max_length=10)

    def __str__(self):
        return self.state_name


class ConstParam(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.IntegerField('任务id', default=0)
    load_m = models.DecimalField('载荷质量（kg）', max_digits=10, decimal_places=3)
    radius = models.DecimalField('半径（m）', max_digits=4, decimal_places=3)
    v_con = models.DecimalField('速度约束（m/s）', max_digits=10, decimal_places=3)
    h_con = models.DecimalField('高度约束（m）', max_digits=10, decimal_places=3)
    q_max = models.DecimalField('动压约束（Pa）', max_digits=10, decimal_places=3)
    theta_last = models.DecimalField('最终角度约束（°）', max_digits=5, decimal_places=3)
    param_name = models.CharField(default='参数变量', max_length=10)

    def __str__(self):
        return self.param_name


class ParamScope(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.IntegerField('任务id', default=0)
    m_l_scope = models.CharField('质量下界数组', max_length=255)
    m_u_scope = models.CharField('质量上界数组', max_length=255)
    p_l_scope = models.CharField('质量下界数组', max_length=255)
    p_u_scope = models.CharField('质量上界数组', max_length=255)
    isp_scope = models.CharField('比冲数组', max_length=255)
    dphi_l_scope = models.CharField('俯仰角控制参数下界数组', max_length=255)
    dphi_u_scope = models.CharField('俯仰角控制参数上界数组', max_length=255)
    alpha_m_scope = models.CharField('攻角绝对值最大值数组', max_length=255)
    a_scope = models.CharField('转弯系数数组', max_length=255)
    scope_name = models.CharField(default='参数范围', max_length=10)

    def __str__(self):
        return self.scope_name


class OptimizedResult(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.IntegerField('任务id', default=0)
    optimized = models.BooleanField('是否是优化结果', default=False)
    t_arr = models.CharField('时间数组', max_length=255)
    v_arr = models.CharField('速度数组', max_length=255)
    phi_arr = models.CharField('程序角数组', max_length=255)
    h_arr = models.CharField('高度数组', max_length=255)
    q_arr = models.CharField('动压数组', max_length=255)
    record_arr = models.CharField('迭代过程数组', max_length=255)
    result_name = models.CharField(default='优化结果', max_length=10)

    def __str__(self):
        return self.result_name


class GA(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.IntegerField('任务id', default=0)
    nind = models.IntegerField('种群规模')
    maxgen = models.IntegerField('进化代数')
    f = models.DecimalField('差分因子', max_digits=3, decimal_places=2)
    xovr = models.DecimalField('交叉概率', max_digits=3, decimal_places=2)
    ga_name = models.CharField(default='GA模型', max_length=10)

    def __str__(self):
        return self.ga_name
