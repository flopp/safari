def load_template(file_name):
    with open('templates/{}'.format(file_name), "r") as f:
        return f.read()


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]
