#!/usr/bin/env python3

import os


def scale_image(source, target, max_dim):
    from PIL import Image, ImageFilter
    blur = ImageFilter.GaussianBlur(int(max_dim/16))
    try:
        with open(source, "rb") as f:
            image = Image.open(f)
            (w, h) = image.size
            if min(w, h) == 0:
                return False, 'SCALING: failed; empty image {0}'.format(source)

            image_rgb = Image.new('RGB', (w, h))
            image_rgb.paste(image, (0, 0))
            image = image_rgb

            small_w, small_h = max_dim, max_dim
            big_w, big_h = max_dim, max_dim
            if w >= h:
                small_h = int((h * max_dim) / w)
                big_w = int((w * max_dim) / h)
            else:
                small_w = int((w * max_dim) / h)
                big_h = int((h * max_dim) / w)

            image_small = image.resize((small_w, small_h), Image.ANTIALIAS)
            image_big = image.resize((big_w, big_h), Image.ANTIALIAS).filter(blur)
            base = Image.new('RGB', (max_dim, max_dim))
            base.paste(image_big, (int((max_dim - big_w)/2), int((max_dim - big_h)/2)))
            base.paste(image_small, (int((max_dim - small_w)/2), int((max_dim - small_h)/2)))
            base.save(target)
            return True, 'SCALING: success {0} -> {1}'.format(source, target)
    except IOError:
        return False, 'SCALING: failed {0}'.format(source)
    except:
        return False, 'SCALING: failed2 {0}'.format(source)


def execute_scale_job(image, thumb, size):
    if os.path.exists(thumb):
        return True, "SCALING: cache hit {0}".format(thumb)
    if not os.path.exists(image):
        return False, "SCALING: failed; source missing {0}".format(image)
    return scale_image(image, thumb, size)


def multithreaded_scaling(processes, job_list):
    import multiprocessing
    pool = multiprocessing.Pool(processes)
    results = [pool.apply_async(execute_scale_job, j) for j in job_list]
    for r in results:
        ok, msg = r.get()
        if not ok:
            print(msg)
