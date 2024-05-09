import re
import dateutil.parser


class SafariCache:
    _code = None
    _internal_id = None
    _name = None
    _url = None
    _coordinates = None
    _owner = None
    _owner_url = None
    _short_description = None
    _description = None
    _preview_image = None
    _founds = 0
    _date = None
    _logs = []

    def load_from_json(self, json_data):
        self._code = json_data['code']
        self._internal_id = json_data['internal_id']
        self._name = json_data['name']
        self._url = json_data['url']
        self._coordinates = json_data['location']
        self._owner = json_data['owner']['username']
        self._owner_url = json_data['owner']['profile_url']
        self._short_description = json_data['short_description']
        self._description = json_data['description']
        self._preview_image = \
            self.determine_image(json_data['preview_image'], json_data['images'], json_data['description'])
        self._founds = int(json_data['founds'])
        self._date = dateutil.parser.parse(json_data['date_created'])

    @staticmethod
    def determine_image(preview_image, images, description):
        if preview_image is not None:
            return u"{0}".format(preview_image['url'])
        elif images is not None and len(images) > 0:
            return u"{0}".format(images[0]['url'])
        else:
            ex = 'src="https?:\/\/www.opencaching.de\/images\/uploads\/(\w+-\w+-\w+-\w+-\w+\.jpg)"'
            match = re.search(ex, description)
            if match:
                return u"https://www.opencaching.de/images/uploads/{0}".format(match.group(1))

            ex = '"images\/uploads\/(\w+-\w+-\w+-\w+-\w+\.jpg)"'
            match = re.search(ex, description)
            if match:
                return u"https://www.opencaching.de/images/uploads/{0}".format(match.group(1))

            ex = '<img [^>]*src="([^"]+)"'
            for match in re.finditer(ex, description):
                url = match.group(1)
                if url.find('resource2') < 0 and url.find('tinymce') < 0:
                    return u"{0}".format(url).replace('&amp;', '&')
        return None

    def clean_description(self):
        # eliminate 'safari box' from description
        self._description = re.sub(r'<div style="[^"]*border:[^"]*background:[^"]*">.*?</div>', '',
                                   self._description, flags=re.MULTILINE | re.DOTALL)

    def to_string(self):
        return u"{0}: {1}, {2}".format(self._code, self._name, self._preview_image)


def load_caches(json_data):
    caches = []
    for code in json_data:
        cache_data = json_data[code]
        if cache_data is not None:
            cache = SafariCache()
            cache.load_from_json(cache_data)
            cache.clean_description()
            caches.append(cache)
    return caches
