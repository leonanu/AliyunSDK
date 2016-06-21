# -*- coding:utf-8 -*-

import sys
import re
import time
import _api


ECS_URL = 'https://ecs.aliyuncs.com'

PAGE_SIZE = 30
RESULT_TIMEWAIT = 5
CONFIRM_TIMEOUT = 30


class ECS(object):
    def __init__(self, access_id, access_secret):
        self.API = _api.AliyunSDK(ECS_URL, access_id, access_secret)

    # Check username legality.
    def check_username(self, account_name):
        if len(account_name) > 16:
            raise SystemExit('The max account name length is 16!')

        elif not re.search(u'^[_a-zA-Z0-9]+$', account_name):
            raise SystemExit('Account name can be only made by 0-9, a-Z and _ !')

        elif not re.search(u'^[a-zA-Z]+$', account_name[0]):
            raise SystemExit('Account name must start with a-Z!')

        else:
            ret = True

        return ret

    # Check password legality.
    def check_password(self, account_pass):
        if (len(account_pass) < 6) or (len(account_pass)) > 32:
            raise SystemExit('The length of password is 6-32!')

        elif not re.search(u'^[_a-zA-Z0-9]+$', account_pass):
            raise SystemExit('Password can be only made by 0-9, a-Z and _ !')

        else:
            ret = True

        return ret

    # Check description legality.
    def check_mark(self, account_mark):
        if (len(account_mark) < 2) or (len(account_mark) > 256):
            raise SystemExit('The length of description is 2-256!')

        elif re.search(u'^http://|^https://', account_mark):
            raise SystemExit('Description can not start with http:// or https://')

        elif not re.search(u'^[_a-zA-Z0-9\-\s]+$', account_mark):
            raise SystemExit('Description can be only made by 0-9, a-Z, _ and - !')

        else:
            ret = True

        return ret

    # Show all reginons of Aliyun.
    def show_region_list(self):
        req = {'Action':'DescribeRegions'}

        res = self.API.request(req)

        ret = set()
        for region in res['Regions']['Region']:
            ret.add(region['RegionId'])

        ret = list(ret)

        return ret

    # Show all instances full list of specific region.
    def show_instance_full_list(self, region_id):
        req = {'Action':'DescribeInstances',
               'RegionId':region_id,
               'PageSize':PAGE_SIZE,
               }

        res = self.API.request(req)

        total_records = res['TotalCount']
        page_num = total_records / PAGE_SIZE

        if page_num == 0:
            page_num = 1

        elif (page_num > 0) and (total_records % PAGE_SIZE != 0):
            page_num += 1

        ret = []
        for page in range(page_num):
            pn = page + 1

            req = {'Action':'DescribeInstances',
                   'RegionId':region_id,
                   'PageSize':PAGE_SIZE,
                   'PageNumber':pn
                   }

            res = self.API.request(req)

            page_list = res['Instances']['Instance']
            for instance in page_list:
                ret.append(instance)

        return ret

    # Show instance monitor information.
    def show_instance_monitor(self, instance_id, start_time, end_time, period):
        req = {'Action':'DescribeInstanceMonitorData',
               'InstanceId':instance_id,
               'StartTime':start_time,
               'EndTime':end_time,
               'Period':period
               }

        res = self.API.request(req)

        ret = res

        return ret


if __name__ == '__main__':
    raise SystemExit()
