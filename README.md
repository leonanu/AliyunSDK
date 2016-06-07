# AliyunSDK [![Build Status](https://travis-ci.org/leonanu/AliyunSDK.svg?branch=master)](https://travis-ci.org/leonanu/AliyunSDK)

AliyunSDK is an Aliyun ECS, SLB and RDS API SDK library, written in Python. 


**Requirement**

Python 2.6/2.7



**Install**
```
python setup.py install
```


                                                                              
**Example:**
```
>>> import AliyunSDK
>>> rds = AliyunSDK.RDS(access_id, access_secret)
>>> ret = rds.show_instance_info(db_instance_id)
>>> pprint.pprint(ret)

{u'AccountMaxQuantity': 500,
 u'AccountType': u'Normal',
 u'AvailabilityValue': u'100.0%',
 u'ConnectionMode': u'Safe',
 u'ConnectionString': u'bp1d2dsj7dh930dn93ze7.mysql.rds.aliyuncs.com',
 u'CreationTime': u'2016-05-31T03:38:05Z',
 u'DBInstanceCPU': u'4',
 u'DBInstanceClass': u'rds.mysql.s3.large',
 u'DBInstanceClassType': u'x',
 u'DBInstanceDescription': u'test_db',
 u'DBInstanceId': u'bp1d2dsj7dh930dn93ze7',
 u'DBInstanceMemory': 8192,
 u'DBInstanceNetType': u'Intranet',
 u'DBInstanceStatus': u'Running',
 u'DBInstanceStorage': 500,
 u'DBInstanceType': u'Primary',
 u'DBMaxQuantity': 500,
 u'Engine': u'MySQL',
 u'EngineVersion': u'5.6',
 u'ExpireTime': u'2016-06-30T16:00:00Z',
 u'InsId': 1,
 u'InstanceNetworkType': u'Classic',
 u'LockMode': u'Unlock',
 u'MaintainTime': u'18:00Z-22:00Z',
 u'MaxConnections': 2000,
 u'MaxIOPS': 5000,
 u'PayType': u'Prepaid',
 u'Port': u'3306',
 u'ReadOnlyDBInstanceIds': {u'ReadOnlyDBInstanceId': []},
 u'RegionId': u'cn-hangzhou',
 u'SecurityIPList': u'10.23.5.6,10.23.4.67',
 u'SupportUpgradeAccountType': u'No',
 u'VpcId': u'',
 u'ZoneId': u'cn-hangzhou-MAZ1(b,c)'}
```
