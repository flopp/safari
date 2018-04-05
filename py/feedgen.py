import os
import datetime
from utilities import load_template


def create_feed(caches, file_name):
    header_template = load_template('atomfeed_header')
    item_template = load_template('atomfeed_item')
    img_template = load_template('atomfeed_item_image')
    footer_template = load_template('atomfeed_footer')
    with open(file_name, 'w') as f:
        f.write(header_template.replace('##DATE##', datetime.datetime.now().isoformat()))
        for cache in caches:
            it = item_template
            it = it.replace('##CODE##', cache._code)
            it = it.replace('##DATE##', cache._date.isoformat())
            it = it.replace('##TITLE##', cache._name)
            it = it.replace('##OWNER##', cache._owner)
            it = it.replace('##DESC##', sanitize_description(cache._description))
            img = ""
            thumb = '.cache/big/{}.jpg'.format(cache._code)
            if os.path.exists(thumb):
                img = img_template.replace('##URL##', 'https://safari.flopp.net/img/big/{}.jpg'.format(cache._code))
            it = it.replace('##IMAGE##', img)
            f.write(it)
        f.write(footer_template)


def sanitize_description(s):
    s = s.replace('\'', '"')
    s = s.replace("href=\"OC", "href=\"https://www.opencaching.de/OC")
    s = s.replace("\"viewcache.php", "\"https://www.opencaching.de/viewcache.php")
    s = s.replace("\"viewprofile.php", "\"https://www.opencaching.de/viewprofile.php")
    s = s.replace("\"images/", "\"https://www.opencaching.de/images/")
    s = s.replace("&quot;images/", "&quot;https://www.opencaching.de/images/")
    s = s.replace("\"resource2/", "\"https://www.opencaching.de/resource2/")
    s = s.replace("\"lib/", "\"https://www.opencaching.de/lib/")
    s = s.replace("\"search.php", "\"https://www.opencaching.de/search.php")
    s = s.replace("\"thumbs.php", "\"https://www.opencaching.de/thumbs.php")
    return s
