# -*- coding:utf-8 -*-

import re
import time
import _api


RDS_URL = 'https://rds.aliyuncs.com'

PAGE_SIZE = 30
RESULT_TIMEWAIT = 5
CONFIRM_TIMEOUT = 30


class RDS(object):
    def __init__(self, access_id, access_secret):
        self.API = _api.AliyunSDK(RDS_URL, access_id, access_secret)

    # Check username legality.
    def check_username(self, account_name):
        if len(account_name) > 16:
            raise SystemExit('The max account name length is 16!')

        if not re.search(u'^[_a-zA-Z0-9]+$', account_name):
            raise SystemExit('Account name can be only made by 0-9, a-Z and _ !')

        if not re.search(u'^[a-zA-Z]+$', account_name[0]):
            raise SystemExit('Account name must start with a-Z!')

    # Check password legality.
    def check_password(self, account_pass):
        if (len(account_pass) < 6) or (len(account_pass)) > 32:
            raise SystemExit('The length of password is 6-32!')

        if not re.search(u'^[_a-zA-Z0-9]+$', account_pass):
            raise SystemExit('Password can be only made by 0-9, a-Z and _ !')

    # Check description legality.
    def check_mark(self, account_mark):
        if (len(account_mark) < 2) or (len(account_mark) > 256):
            raise SystemExit('The length of description is 2-256!')

        if re.search(u'^http://|^https://', account_mark):
            raise SystemExit('Description can not start with http:// or https://')

        if not re.search(u'^[_a-zA-Z0-9\-\s]+$', account_mark):
            raise SystemExit('Description can be only made by 0-9, a-Z, _ and - !')

    # Show all reginons of Aliyun.
    def show_region_list(self):
        req = {'Action':'DescribeRegions'}

        res = self.API.request(req)

        ret = set()
        for region in res['Regions']['RDSRegion']:
            ret.add(region['RegionId'])

        ret = list(ret)

        return ret

    # Show an instance information.
    def show_instance_info(self, instance_id):
        req = {'Action':'DescribeDBInstanceAttribute',
               'DBInstanceId':instance_id
               }

        res = self.API.request(req)

        ret = res['Items']['DBInstanceAttribute'][0]

        return ret

    # Show all instances full list of specific region.
    def show_instance_full_list(self, region_id):
        req = {'Action':'DescribeDBInstances',
               'RegionId':region_id,
               'PageSize':PAGE_SIZE,
               }

        res = self.API.request(req)

        total_records = res['TotalRecordCount']
        page_num = total_records / PAGE_SIZE

        if page_num == 0:
            page_num = 1
        elif (page_num > 0) and (total_records % PAGE_SIZE != 0):
            page_num += 1

        page_list = []
        for page in range(page_num):
            pn = page + 1

            req = {'Action':'DescribeDBInstances',
                   'RegionId':region_id,
                   'PageSize':PAGE_SIZE,
                   'PageNumber':pn
                   }

            res = self.API.request(req)

            page_list.append(res['Items']['DBInstance'])

        ret = []
        for page_instance in page_list:
            for instance in page_instance:
                ret.append(instance)

        return ret

    # Show all instances ID of specific region.
    def show_instance_list(self, region_id):
        instance_full_list = self.show_instance_full_list(region_id)

        ret = []
        for instance_id in instance_full_list:
            ret.append(instance_id['DBInstanceId'])

        return ret

    # Show an instance connection information.
    def show_instance_conn(self, instance_id):
        req = {'Action':'DescribeDBInstanceNetInfo',
               'DBInstanceId':instance_id
               }

        ret = self.API.request(req)

        return ret

    # Show all databases list of specific instances ID.
    def show_db_list(self, instance_id):
        req = {'Action':'DescribeDatabases',
               'DBInstanceId':instance_id
               }

        ret = self.API.request(req)['Databases']['Database']

        return ret

    # Show database information.
    def show_db_info(self, instance_id, db_name):
        req = {'Action':'DescribeDatabases',
               'DBInstanceId':instance_id,
               'DBName':db_name
               }

        ret = self.API.request(req)['Databases']['Database']

        return ret

    # Show all databases name of specific instances ID.
    def show_db_name(self, instance_id):
        full_list = self.show_db_list(instance_id)

        ret = []
        for i in full_list:
            ret.append(i['DBName'])

        return ret

    # Show all accounts list of specific instances ID.
    def show_account_list(self, instance_id):
        req = {'Action':'DescribeAccounts',
               'DBInstanceId':instance_id
               }

        ret = self.API.request(req)['Accounts']['DBInstanceAccount']

        return ret

    # Show account information.
    def show_account_info(self, instance_id, account_name):
        req = {'Action':'DescribeAccounts',
               'DBInstanceId':instance_id,
               'AccountName':account_name
               }

        ret = self.API.request(req)['Accounts']['DBInstanceAccount']

        return ret

    # Show all accounts name of specific instances ID.
    def show_account_name(self, instance_id):
        full_list = self.show_account_list(instance_id)

        ret = []
        for i in full_list:
            ret.append(i['AccountName'])

        return ret

    # Create account of specific instances ID.
    def add_account(self, instance_id, account_name, account_pass, account_mark):
        self.check_username(account_name)
        self.check_password(account_pass)
        self.check_mark(account_mark)

        confirm_timeout = CONFIRM_TIMEOUT

        full_list = self.show_account_name(instance_id)

        if account_name in full_list:
            ret = 'Exist!'

            return ret

        req = {'Action':'CreateAccount',
               'DBInstanceId':instance_id,
               'AccountName':account_name,
               'AccountPassword':account_pass,
               'AccountDescription':account_mark
               }

        ret = self.API.request(req)
        time.sleep(RESULT_TIMEWAIT)

        if ret.has_key('RequestId'):
            ret = ret['RequestId']
        else:
            raise SystemExit('Add account failed!')

        loop = True
        while loop:
            time.sleep(1)

            if account_name in self.show_account_name(instance_id):
                loop = False

            confirm_timeout -= 1
            if confirm_timeout == 0:
                raise SystemExit('Add account timed out!')

        return ret

    # Grant privilege to specific database.
    def grant(self, instance_id, account_name, db_name, priv_type):
        confirm_timeout = CONFIRM_TIMEOUT

        if priv_type == 'ro':
            priv_type = 'ReadOnly'
        elif priv_type == 'rw':
            priv_type = 'ReadWrite'
        else:
            raise SystemExit('Privilege type can be only ro and rw!')

        user_list = self.show_account_name(instance_id)
        if account_name not in user_list:
            raise SystemExit(account_name + ' user not exist! Create first!')

        db_list = self.show_db_name(instance_id)
        if db_name not in db_list:
            raise SystemExit(db_name + ' database not exist!')

        for i in self.show_account_info(instance_id, account_name):
            for k in i['DatabasePrivileges']['DatabasePrivilege']:
                if (k['DBName'] == db_name) and (k['AccountPrivilege'] == priv_type):
                    ret = 'Exist!'

                    return ret

        req = {'Action':'GrantAccountPrivilege',
               'DBInstanceId':instance_id,
               'AccountName':account_name,
               'DBName':db_name,
               'AccountPrivilege':priv_type
               }

        ret = self.API.request(req)
        time.sleep(RESULT_TIMEWAIT)

        if ret.has_key('RequestId'):
            ret = ret['RequestId']
        else:
            ret = False

        loop = True
        while loop:
            time.sleep(1)

            for i in self.show_account_info(instance_id, account_name):
                for k in i['DatabasePrivileges']['DatabasePrivilege']:
                    if (k['DBName'] == db_name) and (k['AccountPrivilege'] == priv_type):
                        loop = False

            confirm_timeout -= 1
            if confirm_timeout == 0:
                raise SystemExit('Grant privilege timed out!')

        return ret

    # Modify account description.
    def change_account_mark(self, instance_id, account_name, account_mark):
        self.check_username(account_name)
        self.check_mark(account_mark)

        confirm_timeout = CONFIRM_TIMEOUT

        for i in self.show_account_info(instance_id, account_name):
            if i['AccountDescription'] == account_mark:
                ret = 'Exist!'

                return ret

        req = {'Action':'ModifyAccountDescription',
               'DBInstanceId':instance_id,
               'AccountName':account_name,
               'AccountDescription':account_mark
               }

        ret = self.API.request(req)
        time.sleep(RESULT_TIMEWAIT)

        if ret.has_key('RequestId'):
            ret = ret['RequestId']
        else:
            ret = False

        loop = True
        while loop:
            time.sleep(1)

            for i in self.show_account_info(instance_id, account_name):
                if i['AccountDescription'] == account_mark:
                    loop = False

            confirm_timeout -= 1
            if confirm_timeout == 0:
                raise SystemExit('Modify account description timed out!')

        return ret


if __name__ == '__main__':
    raise SystemExit()
