#!/usr/local/python2.7/bin/python
# -*- coding:utf-8 -*-

'''
Get all databases in Aliyun, and save them to Excel.
'''


import sys
import xlwt
import AliyunSDK
from multiprocessing.dummy import Pool as ThreadPool


# Aliyun info
access_id = ''
access_secret = ''
region_id_list = ['cn-hangzhou', 'cn-beijing']


class AliRDS(object):
    def __init__(self, access_id, access_secret):
        self.RDS = AliyunSDK.RDS(access_id, access_secret)


    def dbinfo(self, rdsid):
        full_list = self.RDS.show_db_full_list(rdsid)

        return full_list


    def show_databases(self, region_list):
        def gen_dbinfo(rds_id):
            if (rds_id['Engine'] == 'MySQL') and \
               (rds_id['LockMode'] == 'Unlock') and \
               (rds_id['DBInstanceType'] == 'Primary') and \
               (rds_id['DBInstanceStatus'] == 'Running'):
                dbinfo = self.dbinfo(rds_id['DBInstanceId'])

                dbs = []
                for k in dbinfo['Databases']['Database']:
                    dbs.append(
                                {
                                  'DBName':k['DBName'],
                                  'DB-DESC':k['DBDescription'],
                                }
                              )

                dbs_info.append(
                            {
                              'RDS-REGION':rds_id['RegionId'],
                              'RDS-ID':rds_id['DBInstanceId'],
                              'RDS-DESC':rds_id['DBInstanceDescription'],
                              'Databases':dbs,
                            }
                          )

        dbs_info = []
        for region in region_list:
            full_list = self.RDS.show_instance_full_list(region)

            pool = ThreadPool(4)
            results = pool.map(gen_dbinfo, full_list)
            pool.close()
            pool.join()

        return dbs_info


def main():
    p = AliRDS(access_id, access_secret)

    databases = p.show_databases(region_id_list)

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('Databases', cell_overwrite_ok=True)

    # Table header
    headers = ['RDS Region', 'RDS ID', 'RDS Description', 'DB Name', 'DB Description']
    header_num = 0
    for i in headers:
        sheet.write(0, header_num, i)
        header_num += 1

    # Data
    num_row = 1
    for i in databases:
        for k in i['Databases']:
            num_col = 0
            for j in [i['RDS-REGION'], i['RDS-ID'], i['RDS-DESC'], k['DBName'], k['DB-DESC']]:
                if not j.strip():
                    j = 'NULL'

                sheet.write(num_row, num_col, j)
                num_col += 1

            num_row += 1

    book.save('/tmp/databases.xls')
    print 'Saved to /tmp/databases.xls'


if __name__ == '__main__':
    main()
