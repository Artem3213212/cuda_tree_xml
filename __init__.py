
def get_headers(filename, lines):
    '''
    Generates headers in format:
    line_index, header_level, header_text
    '''
    yield (2, 1, 'head-a1')
    yield (4, 2, 'head-b1')
    yield (5, 2, 'head-b2')
    yield (10, 1, 'head-a2')
