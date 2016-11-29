#!/usr/bin/env python3

import json
import re
import os.path
from authdata import *
from okapi import *
from query import *
from safaricache import *
from safarilog import *
from thumbnailer import *
from downloader import *
from sidebargen import *
from dbgen import *
from feedgen import *

CACHE_DIR = "./.cache"
SIZE_BIG=500
SIZE_SMALL=175


def store_json(file_name, json_data):
    with open(file_name, "w") as f:
        f.write(json.dumps(json_data))


def load_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)


def mkdir(d):
    if not os.path.isdir(d):
        os.mkdir(d)


def main():
    okapi = Okapi(OC_OKAPI_KEY)

    mkdir(CACHE_DIR)
    mkdir("{}/json".format(CACHE_DIR))
    mkdir("{}/orig".format(CACHE_DIR))
    mkdir("{}/small".format(CACHE_DIR))
    mkdir("{}/big".format(CACHE_DIR))

    file_name = "{}/json/caches.json".format(CACHE_DIR)
    if os.path.isfile(file_name):
        json_data = load_json(file_name)
    else:
        print("-- downloading query...")
        oc_codes = download_query(OC_USERNAME, OC_PASSWORD, OC_QUERYID)
        json_data = okapi.get_caches(oc_codes, ['code', 'name', 'location', 'status', 'url', 'owner', 'founds', 'date_hidden', 'date_created', 'short_description', 'description', 'images', 'preview_image'])
        store_json(file_name, json_data)

    print("-- analyzing cache data...")
    caches = load_caches(json_data)
    caches = sorted(caches, key=lambda c: c._date, reverse=True)
    print("-- caches: {}".format(len(caches)))

    print("-- analyzing log data...")
    total_logs = 0
    logs_without_coords = 0
    for cache in caches:
        file_name = "{}/json/{}-logs.json".format(CACHE_DIR, cache._code)
        if os.path.isfile(file_name):
            json_data = load_json(file_name)
        else:
            json_data = okapi.get_logs(cache._code, ['uuid', 'date', 'user', 'type', 'comment', 'images'])
            store_json(file_name, json_data)
        cache._logs = load_logs(json_data)

        for log in cache._logs:
            total_logs += 1
            if log._coordinates is None:
                logs_without_coords += 1
    print("-- logs without coordinates: {}/{}".format(logs_without_coords, total_logs))


    print("-- downloading missing images...")
    downloader_jobs = []
    thumbnailer_jobs = []
    for cache in caches:
        if cache._preview_image is not None:
            extension = 'noext'
            m = re.match('^.*\.([^\.]+)$', cache._preview_image)
            if m:
                extension = m.group(1)
            raw_image = '{}/{}/{}.{}'.format(CACHE_DIR, "orig", cache._code, extension)
            if not os.path.exists(raw_image):
                downloader_jobs.append((cache._preview_image, raw_image))
            thumb_small = '{}/{}/{}.jpg'.format(CACHE_DIR, "small", cache._code)
            if not os.path.exists(thumb_small):
                thumbnailer_jobs.append((raw_image, thumb_small, SIZE_SMALL))
            thumb_big = '{}/{}/{}.jpg'.format(CACHE_DIR, "big", cache._code)
            if not os.path.exists(thumb_big):
                thumbnailer_jobs.append((raw_image, thumb_big, SIZE_BIG))
    multithreaded_downloading(4, downloader_jobs)

    print("-- scaling images...")
    multithreaded_scaling(4, thumbnailer_jobs)

    print("-- creating db...")
    create_db(caches, ".cache/safari.sqlite")

    print("-- create feed...")
    create_feed(caches, ".cache/feed.xml")

    print("-- creating sidebar...")
    create_sidebar(caches, ".cache/sidebar.html")


if __name__ == '__main__':
    main()
