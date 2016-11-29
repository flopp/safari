#!/usr/bin/env python3

import os
import requests


def download_if_not_exists(url, target):
    if not os.path.exists(target):
        try:
            response = requests.get(url)
            with open(target, 'wb') as f:
                f.write(response.content)
            return True, 'DOWNLOAD: success {0} -> {1}'.format(url, target)
        except IOError as e:
            return False, 'DOWNLOAD: failed {0} {1}'.format(url, e)
    else:
        return True, 'DOWNLOAD: cache hit {0}'.format(target)


def multithreaded_downloading(processes, job_list):
    import multiprocessing
    pool = multiprocessing.Pool(processes)
    results = [pool.apply_async(download_if_not_exists, j) for j in job_list]
    for r in results:
        ok, msg = r.get()
        if not ok:
            print(msg)
