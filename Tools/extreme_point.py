def extreme_points(pixels_coord, direction) -> list:
    x_pixels_coord = list(map(lambda pixel_coord: pixel_coord[0], pixels_coord))
    x_extreme_points = set(x_pixels_coord)
    extreme_side = 0

    if direction == -1:
        extreme_side = min(x_extreme_points)

    elif direction == 1:
        extreme_side = max(x_extreme_points)

    return get_extreme_pixels(pixels_coord, extreme_side)


def get_extreme_pixels(pixels_coord, extreme_side) -> list:
    pixels = []

    for x, y in pixels_coord:
        if x == extreme_side:
            pixels.append((x, y))

    return pixels
