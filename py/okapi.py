#!/usr/bin/env python3

import requests
import json

class Okapi:
    _base_url = 'https://www.opencaching.de/okapi/'
    _consumer_key = None
    
    def __init__(self, okapi_key):
        self._consumer_key = okapi_key
    
    def get_server_stats(self):
        url = self._base_url + 'services/apisrv/stats'
        data = {'consumer_key' : self._consumer_key}
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}        
        r = requests.post(url, json=data, headers=headers)
        return r.json()
    
    def get_replication_info(self):
        url = self._base_url + 'services/replicate/info'
        r = requests.post(url, params={'consumer_key' : self._consumer_key})
        return r.json()
        
    def get_caches(self, codes, fields):
        print("-- downloading cache details...")
        url = self._base_url + 'services/caches/geocaches'
        caches = {}
        for code_chunk in self.chunks(codes, 100):
            data = {
                'consumer_key' : self._consumer_key, 
                'cache_codes' : '|'.join(code_chunk),
                'fields' : '|'.join(fields)
            }
            headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Accept-Charset': 'utf-8'}
            r = requests.post(url, data=data)
            caches.update(r.json())
        return caches
    
    def get_logs(self, cache_code, fields):
        #print("-- downloading logs for cache {}...".format(cache_code))
        url = self._base_url + 'services/logs/logs'
        data = {
            'consumer_key' : self._consumer_key, 
            'cache_code' : cache_code,
            'fields' : '|'.join(fields)
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Accept-Charset': 'utf-8'}
        r = requests.post(url, data=data)
        return r.json()
    
    def chunks(self, l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in range(0, len(l), n):
            yield l[i:i+n]
