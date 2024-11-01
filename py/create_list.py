import math
import os
from utilities import chunks, load_template

def create_file_name(index, count):
    if index < 0 or index >= count:
        return None
    elif index == 0:
        return 'list.html'
    return f'list{index}.html'


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


def create_cache_item(template, cache, target_dir):
    desc = ''
    if cache._short_description is not None:
        desc = cache._short_description
    finds = f'{cache._founds} Funde'
    if cache._founds is 0:
        finds = 'keine Funde'
    elif cache._founds is 1:
        finds = 'ein Fund'
    with_coords = 0
    for log in cache._logs:
        if log._coordinates:
            with_coords += 1
    finds2 = f'{with_coords} Logs mit Koordinaten'
    if with_coords == 0:
        finds2 = 'keine Logs mit Koordinaten'
    elif with_coords == 1:
        finds2 = 'ein Log mit Koordinaten'
    return template \
        .replace('##OCCODE##', cache._code)\
        .replace('##NAME##', cache._name)\
        .replace('##OWNER##', cache._owner)\
        .replace('##DATE##', cache._date.strftime('%Y-%m-%d'))\
        .replace('##FINDS##', finds)\
        .replace('##FINDS2##', finds2)\
        .replace('##DESCRIPTION##', desc)


def createlist(caches, chunk_size, target_dir):
    header_template = load_template('list_header')
    footer_template = load_template('list_footer')
    item_template = load_template('list_item')

    chunk_count = int(math.ceil(len(caches) / chunk_size))
    for chunk_index, chunk_caches in enumerate(chunks(caches, chunk_size)):
        target_file_name = os.path.join(target_dir, create_file_name(chunk_index, chunk_count))
        pagination = create_pagination(chunk_index, chunk_count)
        with open(target_file_name, 'w') as f:
            prev = create_file_name(chunk_index - 1, chunk_count)
            next = create_file_name(chunk_index + 1, chunk_count)
            f.write(header_template
                    .replace('##PREVLINK##', f'<link rel="prev" href="{prev}">' if prev else '')
                    .replace('##NEXTLINK##', f'<link rel="next" href="{next}">' if next else '')
                    .replace('##PAGINATION##', pagination)
                    )
            for cache in chunk_caches:
                f.write(create_cache_item(item_template, cache, target_dir))
            f.write(footer_template.replace('##PAGINATION##', pagination))
