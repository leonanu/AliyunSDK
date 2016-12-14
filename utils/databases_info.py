#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import xlwt
from AliyunSDK import rds
from multiprocessing.dummy import Pool as ThreadPool


# Aliyun info
access_id = ''
access_secret = ''
region_id_list = ['cn-hangzhou']


class AliRDS(object):
    def __init__(self, access_id, access_secret):
        self.RDS = rds.AliyunRDS(access_id, access_secret)


    def dbinfo(self, rdsid):
        full_list = self.RDS.show_db_list(rdsid)

        return full_list

    def netinfo(self, rdsid):
        rdsnetinfo = self.RDS.show_instance_netinfo(rdsid)

        return rdsnetinfo

    def show_databases(self, region_list):
        def gen_dbinfo(rds_id):
            if (rds_id['Engine'] == 'MySQL') and \
               (rds_id['LockMode'] == 'Unlock') and \
               (rds_id['DBInstanceType'] == 'Primary') and \
               (rds_id['DBInstanceStatus'] == 'Running'):
                dbinfo = self.dbinfo(rds_id['DBInstanceId'])
                coninfo = self.netinfo(rds_id['DBInstanceId'])

                rds_ip_lan = ''
                rds_conn_lan = ''
                rds_port_lan = ''
                rds_ip_wan = ''
                rds_conn_wan = ''
                rds_port_wan = ''

                for network in coninfo['DBInstanceNetInfos']['DBInstanceNetInfo']:
                    rds_vpcid = network['VPCId']
                    if network['IPType'] == 'Inner' or network['IPType'] == 'Private':
                        rds_ip_lan = network['IPAddress']
                        rds_conn_lan = network['ConnectionString']
                        rds_port_lan = network['Port']
                    elif network['IPType'] == 'Public':
                        rds_ip_wan = network['IPAddress']
                        rds_conn_wan = network['ConnectionString']
                        rds_port_wan = network['Port']

                rds_type = coninfo['InstanceNetworkType']

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
                              'RDS-TYPE':rds_type,
                              'RDS-VPCID':rds_vpcid,
                              'RDS-IP-LAN':rds_ip_lan,
                              'RDS-CONN-LAN':rds_conn_lan,
                              'RDS-PORT-LAN':rds_port_lan,
                              'RDS-IP-WAN':rds_ip_wan,
                              'RDS-CONN-WAN':rds_conn_wan,
                              'RDS-PORT-WAN':rds_port_wan,
                              'RDS-DESC':rds_id['DBInstanceDescription'],
                              'Databases':dbs,
                            }
                          )

        dbs_info = []
        for region in region_list:
            full_list = self.RDS.show_instance_list(region)

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
    headers = ['RDS Region',
               'RDS ID',
               'RDS Description',
               'RDS Network Type',
               'RDS VPC ID',
               'RDS LAN IP',
               'RDS LAN Connection',
               'RDS LAN Port',
               'RDS WAN IP',
               'RDS WAN Connection',
               'RDS WAN Port',
               'DB Name',
               'DB Description']

    header_num = 0
    for i in headers:
        sheet.write(0, header_num, i)
        header_num += 1

    # Data
    num_row = 1
    for i in databases:
        for k in i['Databases']:
            num_col = 0
            for j in [i['RDS-REGION'], i['RDS-ID'], i['RDS-DESC'], i['RDS-TYPE'], i['RDS-VPCID'], i['RDS-IP-LAN'], i['RDS-CONN-LAN'], i['RDS-PORT-LAN'], i['RDS-IP-WAN'], i['RDS-CONN-WAN'], i['RDS-PORT-WAN'], k['DBName'], k['DB-DESC']]:
                if not j.strip():
                    j = ' '

                sheet.write(num_row, num_col, j)
                num_col += 1

            num_row += 1

    book.save('/tmp/databases.xls')
    print 'Saved to /tmp/databases.xls'


if __name__ == '__main__':
    main()
