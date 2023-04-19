def idx_to_cata(idx):
    cata = -1
    if 100 <= idx < 201:
        cata = 100
    elif 201 <= idx < 401:
        cata = 201
    elif 401 <= idx < 601:
        cata = 401
    elif 601 <= idx < 1000:
        cata = 601
    return cata


def find_certain_line(lines, substring):
    for idx, line in enumerate(lines):
        if substring in line:
            return idx
    return -1


def insert_certain_lines(pos, old, lines):
    new = []
    head = old[:pos]
    tail = old[pos:]
    new.extend(head)
    new.extend(lines)
    new.extend(tail)
    return new
