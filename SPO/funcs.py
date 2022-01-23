def getKey(d, value, i=-1):
    k = list(d.keys())[i + 1:]
    for k1 in k:
        if d.get(k1) == value:
            return k1

    return None
