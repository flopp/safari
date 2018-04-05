import requests
import re


def download_query(user, password, queryid):
    headers = {'User-agent': 'safari-map [https://safari.flopp.net/]'}
    s = requests.Session()
    r = s.post(
        'https://www.opencaching.de/login.php',
        data={
            'action': 'login',
            'target': 'query.php',
            'email': user.encode('utf-8'),
            'password': password.encode('utf-8')
        },
        headers=headers
    )

    if '32x32-search.png' not in r.text:
        print("ERROR: failed to log in (bad response)")
        return []

    oc_codes = []
    batch_size = 20
    batch_start = 0
    while True:
        url = 'https://www.opencaching.de/search.php?queryid={}&output=loc&startat={}&count={}&zip=0'
        url = url.format(queryid, batch_start, batch_size)
        r = s.get(url, headers=headers)
        if r.status_code != 200:
            print("-- Terminating due to bad status code: {}".format(r.status_code))
            break
        new_oc_codes = []
        for m in re.finditer(r'<name id="([^"]+)">', r.text):
            new_oc_codes.append(m.groups()[0])
        if len(new_oc_codes) == 0:
            break
        oc_codes = oc_codes + new_oc_codes
        batch_start += batch_size

    return oc_codes
