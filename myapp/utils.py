from django.core import serializers


def serialize_object(o):
    return serializers.serialize('json', o)


def str2int_arr(str: str):
    return_str = str.split(',')
    return_arr = []
    for i in range(len(return_str)):
        return_arr.append(int(return_str[i]))
    return return_arr


def str2float_arr(str: str, pre=3):
    return_str = str.split(',')
    return_arr = []
    for i in range(len(return_str)):
        return_arr.append(round(float(return_str[i]), pre))
    return return_arr


def arr2str(arr: list):
    length = arr.__len__()
    str = ''
    for i in range(length):
        if i == length - 1:
            str = str + arr[i].__str__()
        else:
            str = str + arr[i].__str__() + ','
    return str


def get_initial_state(body_dist: dict):
    return body_dist['taskParam']['initialState']


def get_param_scope(body_dict: dict):
    return body_dict['taskParam']['paramScope']


def get_task(body_dict: dict):
    return body_dict['taskParam']['task']


def get_const_param(body_dict: dict):
    return body_dict['taskParam']['constParam']


def get_GA(body_dict: dict):
    return body_dict['taskParam']['GA']
