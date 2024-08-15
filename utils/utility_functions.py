from datetime import datetime
import re

def parse_value(value):
    value = value.strip()
    if value.startswith('$'):
        value = re.sub(r'[^\d.-]', '', value[1:])

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return datetime.strptime(value, "%b %d, %Y")
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value

def sort_tree(tree, col, reverse):
    items = [(tree.set(row, col), row) for row in tree.get_children('')]

    items.sort(key=lambda t: parse_value(t[0]), reverse=reverse)

    for index, (val, row) in enumerate(items):
        tree.move(row, '', index)

    tree.heading(col, command=lambda: sort_tree(tree, col, not reverse))