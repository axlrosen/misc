
def x(loc):
    return loc[0]

def y(loc):
    return loc[1]

def to_grid(p, loc):
    return x(loc) + p.width * y(loc)

def value(p, loc):
    return p.fill[to_grid(p, loc)]

def is_open(p, loc):
    return value(p, loc) != '.'

def across_length(p, loc):
    if x(loc) != 0 and is_open(p, [x(loc)-1, y(loc)]):
        return 0
    loc = loc.copy()
    result = 0
    while x(loc) < p.width and is_open(p, loc):
        loc[0] += 1
        result += 1
    return result

def down_length(p, loc):
    if y(loc) != 0 and is_open(p, [x(loc), y(loc)-1]):
        return 0
    loc = loc.copy()
    result = 0
    while y(loc) < p.height and is_open(p, loc):
        loc[1] += 1
        result += 1
    return result

def across_entry(p, loc):
    if x(loc) != 0 and is_open(p, [x(loc)-1, y(loc)]):
        return None
    loc = loc.copy()
    result = ""
    while x(loc) < p.width and is_open(p, loc):
        result += p.solution[to_grid(p, loc)]
        loc[0] += 1
    return result

def down_entry(p, loc):
    if y(loc) != 0 and is_open(p, [x(loc), y(loc)-1]):
        return None
    loc = loc.copy()
    result = ""
    while y(loc) < p.height and is_open(p, loc):
        result += p.solution[to_grid(p, loc)]
        loc[1] += 1
    return result

def all_entries(p):
    result = []
    for i in range(0,p.width):
        for j in range(0, p.height):
            across = across_entry(p, [i, j])
            if across: result.append(across)
            down = down_entry(p, [i, j])
            if down: result.append(down)
    return result

def count_threes(p):
    count = 0
    for i in range(0,p.width):
        for j in range(0, p.height):
            if across_length(p, [i, j]) == 3:
                count += 1
            if down_length(p, [i, j]) == 3:
                count += 1
    return count

def find_left(p, desired_length):
    result = None
    for y in range(0, p.height-1):
        if across_length(p, [0, y]) == desired_length:
            if result:
                return None
            result = [0, y]
    return result

def find_right(p, desired_length):
    result = None
    for y in range(0, p.height-1):
        loc = [p.width - desired_length, y]
        if across_length(p, loc) == desired_length:
            if result:
                return None
            result = loc
    return result

def fill_across(p, loc, entry):
    loc = loc.copy()
    for c in entry:
        if loc[0] == p.width:
            raise ValueError
        i = to_grid(p, loc)
        p.fill = p.fill[:i] + c + p.fill[i+1:]
        loc[0] += 1

def fill_down(p, loc, entry):
    loc = loc.copy()
    for c in entry:
        if loc[1] == p.height:
            raise ValueError
        i = to_grid(p, loc)
        p.fill = p.fill[:i] + c + p.fill[i+1:]
        loc[1] += 1

def find_longest_downs(p):
    n = 0
    d1_loc = d2_loc = None
    for x in range(0, p.width-1):
        for y in range(0, p.height-5):
            l = down_length(p, [x,y])
            if l > n:
                d1_loc = [x,y]
                d2_loc = None
                n = l
            elif l == n:
                d2_loc = [x,y]
    return d1_loc, d2_loc

def fits_across(p, loc, entry):
    if entry in p.added:
        return False
    loc = loc.copy()
    for c in entry:
        v = value(p, loc)
        if v != c and v != '-':
            return False
        loc[0] += 1
    return True

def fits_down(p, loc, entry):
    if entry in p.added:
        return False
    loc = loc.copy()
    for c in entry:
        v = value(p, loc)
        if v != c and v != '-':
            return False
        loc[1] += 1
    return True
