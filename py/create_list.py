import math
import os
from utilities import chunks, load_template

NO_IMAGE_DATA = \
    "data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22500%22%20height%3D%22500%22%20xmlns%3D%22http%3A" \
    "%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20500%20500%22%20preserveAspectRatio%3D%22none%" \
    "22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_16296b729b2%20text%20%7B%20fill%3A%23ec" \
    "eeef%3Bfont-weight%3Abold%3Bfont-family%3AArial%2C%20Helvetica%2C%20Open%20Sans%2C%20sans-serif%2C%20" \
    "monospace%3Bfont-size%3A40pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_16296b729b2%22%" \
    "3E%3Crect%20width%3D%22500%22%20height%3D%22500%22%20fill%3D%22%2355595c%22%3E%3C%2Frect%3E%3Cg%3E%3C" \
    "text%20x%3D%22100%22%20y%3D%22250%22%3EKein%20Bild%20%3A(%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E"

def create_file_name(index, count):
    if index < 0 or index >= count:
        return None
    elif index == 0:
        return 'list.html'
    return 'list{}.html'.format(index)


def create_pagination(index, count):
    r = '''
        <div class="text-center">
        <nav>
            <ul class="pagination">
        '''
    if index > 0:
        r += '<li class="page-item"><a class="page-link" href="{}"><i class="fa fa-chevron-left"></i></a></li>'\
            .format(create_file_name(index - 1, count))
    else:
        r += '<li class="page-item disabled"><a class="page-link" href="#"><i class="fa fa-chevron-left"></i></a></li>'
    if index > 1:
        r += '<li class="page-item"><a class="page-link" href="{}">{}</a></li>'\
            .format(create_file_name(0, count), 0)
    if index > 2:
        r += '<li class="page-item disabled"><a class="page-link" href="#"><i class="fa fa-ellipsis-h"></i></a></li>'
    if index > 0:
        r += '<li class="page-item"><a class="page-link" href="{}">{}</a></li>'\
            .format(create_file_name(index - 1, count), index - 1)
    r += '<li class="page-item active"><a class="page-link" href="#">{}</a></li>'\
        .format(index)
    if index + 1 < count:
        r += '<li class="page-item"><a class="page-link" href="{}">{}</a></li>'\
            .format(create_file_name(index + 1, count), index + 1)
    if index + 3 < count:
        r += '<li class="page-item disabled"><a class="page-link" href="#"><i class="fa fa-ellipsis-h"></i></a></li>'
    if index + 2 < count:
        r += '<li class="page-item"><a class="page-link" href="{}">{}</a></li>'\
            .format(create_file_name(count - 1, count), count - 1)
    if index + 1 < count:
        r += '<li class="page-item"><a class="page-link" href="{}"><i class="fa fa-chevron-right"></i></a></li>'\
            .format(create_file_name(index + 1, count))
    else:
        r += '<li class="page-item disabled"><a class="page-link" href="#"><i class="fa fa-chevron-right"></i></a></li>'

    r += '''</ul>
        </nav>
        </div>
        '''
    return r


def create_cache_item(template, cache):
    desc = ''
    if cache._short_description is not None:
        desc = cache._short_description
    img = NO_IMAGE_DATA
    thumb = '.cache/big/{}.jpg'.format(cache._code)
    if os.path.exists(thumb):
        img = 'img/big/{}.jpg'.format(cache._code)
    finds = '{} Funde'.format(cache._founds)
    if cache._founds is 0:
        finds = 'keine Funde'
    elif cache._founds is 1:
        finds = 'ein Fund'
    with_coords = 0
    for log in cache._logs:
        if log._coordinates:
            with_coords += 1
    finds2 = '{} Logs mit Koordinaten'.format(with_coords)
    if with_coords == 0:
        finds2 = 'keine Logs mit Koordinaten'
    elif with_coords == 1:
        finds2 = 'ein Log mit Koordinaten'
    return template \
        .replace('##OCCODE##', cache._code)\
        .replace('##NAME##', cache._name)\
        .replace('##IMG##', img)\
        .replace('##OWNER##', cache._owner)\
        .replace('##DATE##', cache._date.strftime('%Y-%m-%d'))\
        .replace('##FINDS##', finds)\
        .replace('##FINDS2##', finds2)\
        .replace('##DESCRIPTION##', desc)


def createlist(caches, chunk_size):
    header_template = load_template('list_header')
    footer_template = load_template('list_footer')
    item_template = load_template('list_item')

    chunk_count = int(math.ceil(len(caches) / chunk_size))
    for chunk_index, chunk_caches in enumerate(chunks(caches, chunk_size)):
        target_file_name = '.cache/' + create_file_name(chunk_index, chunk_count)
        pagination = create_pagination(chunk_index, chunk_count)
        with open(target_file_name, 'w') as f:
            prev = create_file_name(chunk_index - 1, chunk_count)
            next = create_file_name(chunk_index + 1, chunk_count)
            f.write(header_template
                    .replace('##PREVLINK##', '<link rel="prev" href="{}">'.format(prev) if prev else '')
                    .replace('##NEXTLINK##', '<link rel="next" href="{}">'.format(next) if next else '')
                    .replace('##PAGINATION##', pagination)
                    )
            for cache in chunk_caches:
                f.write(create_cache_item(item_template, cache))
            f.write(footer_template.replace('##PAGINATION##', pagination))
