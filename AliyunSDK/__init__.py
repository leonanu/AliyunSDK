# -*- coding:utf-8 -*-

'''
AliyunSDK
=========
AliyunSDK is an Aliyun ECS, SLB and RDS API SDK library, written in Python.

Example:
    >>> import AliyunSDK
    >>> rds = AliyunSDK.RDS(access_id, access_secret)
    >>> ret = rds.show_instance_info(db_instance_id)
    >>> print ret
'''

from rds import RDS
from ecs import ECS


__title__ = 'AliyunSDK'
__author__ = 'Nanu'
