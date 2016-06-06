# -*- coding:utf-8 -*-

import re
import sys
import urllib
import urllib2
import time
import datetime
import json
import base64
import hmac
import uuid
from hashlib import sha1


ECS_VERSION = '2014-05-26'
RDS_VERSION = '2014-08-15'
SLB_VERSION = '2014-05-15'

LOG_FILE = './AliyunSDK.log'
REQUEST_RETRY = 3
REQUEST_RETRY_INTERVAL = 3


class AliyunSDK(object):
    def __init__(self, url, access_id, access_secret):
        self.url = url
        self.access_id = access_id
        self.access_secret = access_secret

        product = re.findall(u'\/\/(.*?)\.aliyuncs', self.url)
        if product[0] == 'ecs':
            self.version = ECS_VERSION
        elif product[0] == 'rds':
            self.version = RDS_VERSION
        elif product[0] == 'slb':
            self.version = SLB_VERSION
        else:
            error = 'Invalid Aliyun API URL!\nOnly ECS/RDS/SLB are supported!'
            raise SystemExit(error)

    # API Log
    def _api_log(self, log_content):
        datetime_now = str(datetime.datetime.now())

        try:
            log_fd = open(LOG_FILE, 'a+')

        except Exception as e:
            raise SystemExit(e)

        try:
            log_fd.write(datetime_now + '\n')
            log_fd.write('='*len(datetime_now) + '\n')
            for i in log_content:
                log_fd.write(str(i) + '\n')
            log_fd.write('\n'*2)

        except Exception as e:
            print e

        finally:
            log_fd.close()

    # Aliyun Signature.
    def sign(self, access_key_secret, parameters):
        sorted_parameters = sorted(parameters.items(),
                                   key=lambda parameters: parameters[0])
        canonicalized_query_string = ''
        for (k, v) in sorted_parameters:
            canonicalized_query_string += '&' + self.char_encode(k) + '=' + self.char_encode(v)

        string_to_sign = 'GET&%2F&' + self.char_encode(canonicalized_query_string[1:])

        h = hmac.new(access_key_secret + '&', string_to_sign, sha1)
        signature = base64.encodestring(h.digest()).strip()

        return signature

    # Encode URL chars.
    def char_encode(self, encodeStr):
        encodeStr = str(encodeStr)
        res = urllib.quote(encodeStr.decode(sys.stdin.encoding).encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')

        return res

    # Generate request URL.
    def make_request(self, params):
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%Sz', time.gmtime())
        parameters = {
                      'Format':'JSON',
                      'Version':self.version,
                      'AccessKeyId':self.access_id,
                      'SignatureVersion':'1.0',
                      'SignatureMethod':'HMAC-SHA1',
                      'SignatureNonce':str(uuid.uuid1()),
                      'TimeStamp':timestamp
                     }

        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(self.access_secret, parameters)
        parameters['Signature'] = signature
        url = self.url + '/?' + urllib.urlencode(parameters)

        return url

    # GET request URL.
    def request(self, params):
        attempt = 1
        retry = True
        while retry:
            try:
                url = self.make_request(params)
                req = urllib2.Request(url)

                conn = urllib2.urlopen(req)
                response = conn.read()

                obj = json.loads(response)

                retry = False

            except Exception as e:
                log = []
                log.append('Request URL: ' + str(url))
                log.append('Got Error: ' + str(e))
                log.append('Retry ... ' + '[' + str(attempt) + '/' + str(REQUEST_RETRY) + ']')
                self._api_log(log)

                time.sleep(REQUEST_RETRY_INTERVAL)
                attempt += 1
                if attempt == REQUEST_RETRY + 1:
                    raise SystemExit(e)

        return obj


if __name__ == '__main__':
    raise SystemExit()
