#!/usr/bin/env python3

import datetime
import os


def load_template(file_name):
    with open('templates/{}'.format(file_name), "r") as f:
        return f.read()


def create_sidebar(caches, target):
    header_template = load_template('sidebar_header')
    item_template = load_template('sidebar_item')
    img_template = load_template('sidebar_img')
    desc_template = load_template('sidebar_desc')
    footer_template = load_template('sidebar_footer')
    with open (target, 'w') as f:
        f.write(header_template.replace('##COUNT##', str(len(caches))))
        for cache in caches:
            it = item_template
            it = it.replace('##CODE##', cache._code)
            it = it.replace('##DATE##', cache._date.strftime('%Y-%m-%d'))
            it = it.replace('##NAME##', cache._name)
            it = it.replace('##OWNER##', cache._owner)
            it = it.replace('##URL##', cache._url)

            finds = '{} Funde'.format(cache._founds)
            if cache._founds is 0:
                finds = 'keine Funde'
            elif cache._founds is 1:
                finds = 'ein Fund'
            it = it.replace('##FINDS##', finds)

            with_coords = 0
            for log in cache._logs:
                if log._coordinates:
                    with_coords += 1
            finds2 = '{} Logs mit Koordinaten'.format(with_coords)
            if with_coords == 0:
                finds2 = 'keine Logs mit Koordinaten'
            elif with_coords == 1:
                finds2 = 'ein Log mit Koordinaten'
            it = it.replace('##FINDS2##', finds2)

            desc = ''
            if cache._short_description is not None:
                desc = desc_template.replace('##TEXT##', cache._short_description)
            it = it.replace('##DESC##', desc)

            img = ''
            thumb = '.cache/small/{}.jpg'.format(cache._code)
            if os.path.exists(thumb):
                img = img_template.replace('##URL##', 'img/small/{}.jpg'.format(cache._code))
            it = it.replace('##IMG##', img)
            f.write(it)
        f.write(footer_template.replace('##DATE##', datetime.datetime.now().isoformat()))
