import argparse
import json
import os
import re

from authdata import OC_OKAPI_KEY, OC_USERNAME, OC_PASSWORD, OC_QUERYID
from okapi import Okapi
from query import download_query
from safaricache import load_caches
from safarilog import load_logs
from thumbnailer import Thumbnailer
from downloader import Downloader
from sidebargen import create_sidebar
from dbgen import create_db, collect_logs
from create_list import createlist
from feedgen import create_feed


USER_AGENT = 'safari-map [https://safari.flopp.net/]'
MANUAL_CACHES_FILE = "./static/manual-caches.txt"
SIZE_BIG = 500
SIZE_SMALL = 175


def store_json(file_name, json_data):
    with open(file_name, "w") as f:
        f.write(json.dumps(json_data))


def load_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)


def main(cache_dir):
    okapi = Okapi(OC_OKAPI_KEY, user_agent=USER_AGENT)

    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(os.path.join(cache_dir, "json"), exist_ok=True)
    os.makedirs(os.path.join(cache_dir, "orig"), exist_ok=True)
    os.makedirs(os.path.join(cache_dir, "small"), exist_ok=True)
    os.makedirs(os.path.join(cache_dir, "big"), exist_ok=True)

    file_name = os.path.join(cache_dir, "json", "caches.json")
    if os.path.isfile(file_name):
        json_data = load_json(file_name)
    else:
        print("-- downloading query...")
        oc_codes = download_query(OC_USERNAME, OC_PASSWORD, OC_QUERYID)
        try:
            with open(MANUAL_CACHES_FILE, "r") as f:
                for oc_code in f:
                    oc_code = oc_code.strip()
                    if oc_code.startswith("OC"):
                        print("-- adding manual code {}".format(oc_code))
                        oc_codes.append(oc_code)
        except IOError:
            pass

        print("-> codes: {}".format(len(oc_codes)))
        fields = ['code', 'name', 'location', 'status', 'url', 'owner', 'founds', 'date_hidden', 'date_created',
                  'short_description', 'description', 'images', 'preview_image', 'internal_id']
        json_data = okapi.get_caches(oc_codes, fields)
        store_json(file_name, json_data)

    print("-- analyzing cache data...")
    caches = load_caches(json_data)
    caches = sorted(caches, key=lambda c: c._date, reverse=True)
    print("-> caches: {}".format(len(caches)))

    print("-- analyzing log data...")
    total_logs = 0
    logs_without_coords = 0
    for cache in caches:
        file_name = os.path.join(cache_dir, "json", f"{cache._code}-logs.json")
        if os.path.isfile(file_name):
            json_data = load_json(file_name)
        else:
            fields = ['uuid', 'date', 'user', 'type', 'comment', 'images', 'internal_id']
            json_data = okapi.get_logs(cache._code, fields)
            store_json(file_name, json_data)
        print(f"CACHE {cache._code}")
        cache._logs = load_logs(json_data)

        for log in cache._logs:
            total_logs += 1
            if log._coordinates is None:
                logs_without_coords += 1
    print("-- logs without coordinates: {}/{}".format(logs_without_coords, total_logs))

    print("-- downloading missing images...")
    downloader = Downloader(threads=4, user_agent=USER_AGENT)
    thumbnailer = Thumbnailer(threads=4)
    for cache in caches:
        if cache._preview_image is not None:
            extension = 'noext'
            m = re.match('^.*\.([^.\?]+)(\?.*)?$', cache._preview_image)
            if m:
                extension = m.group(1)
            raw_image = '{}/{}/{}.{}'.format(cache_dir, "orig", cache._code, extension)
            downloader.add_job(cache._preview_image, raw_image)
            thumb_small = '{}/{}/{}.jpg'.format(cache_dir, "small", cache._code)
            thumbnailer.add_job(raw_image, thumb_small, SIZE_SMALL)
            thumb_big = '{}/{}/{}.jpg'.format(cache_dir, "big", cache._code)
            thumbnailer.add_job(raw_image, thumb_big, SIZE_BIG)
    downloader.run()

    print("-- scaling images...")
    thumbnailer.run()

    print("-- creating files...")
    create_db(caches, os.path.join(cache_dir, "safari.sqlite"))
    collect_logs(caches, os.path.join(cache_dir, "log-data.js"))
    createlist(caches, 30, cache_dir)
    create_feed(caches, os.path.join(cache_dir, "feed.xml"))
    create_sidebar(caches, "static/index.html", os.path.join(cache_dir, "index.html"), cache_dir)


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--cache-dir",
        dest="cache_dir",
        metavar="DIR",
        type=str
    )
    args = args_parser.parse_args()

    main(args.cache_dir)
