def extreme_point(lists, direction):
    ys = set(i[0][1] for i in lists)
    dots = []

    for i in ys:
        for k in lists:
            if k[0][1] == i:
                dots.append((i, [k[0][0]]))

    if direction == 1:
        return [[i[0], max(i[1])] for i in dots]

    else:
        return [[i[0], min(i[1])] for i in dots]
