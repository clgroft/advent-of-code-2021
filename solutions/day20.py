from collections import defaultdict


class Image:
    def __init__(self, lines=None, light_background=False):
        self._light_background = light_background
        self._pixels = defaultdict(lambda: '#' if light_background else '.')
        if lines:
            for y, line in enumerate(lines):
                for x, pixel in enumerate(line.strip()):
                    self.set_pixel(x, y, pixel)

    def borders(self):
        xmin, xmax, ymin, ymax = 0, 0, 0, 0
        for x, y in self._pixels.keys():
            if x < xmin: xmin = x
            if x > xmax: xmax = x
            if y < ymin: ymin = y
            if y > ymax: ymax = y
        return xmin, xmax, ymin, ymax

    def code_at_pixel(self, x, y):
        code = 0
        keys = [(x-1, y-1), (x, y-1), (x+1, y-1),
                (x-1, y),   (x, y),   (x+1, y),
                (x-1, y+1), (x, y+1), (x+1, y+1)]
        for a, b in keys:
            code *= 2
            if self._pixels[(a,b)] == '#':
                code += 1
        return code

    def code_in_background(self):
        return 511 if self._light_background else 0

    def set_pixel(self, x, y, pixel):
        self._pixels[(x,y)] = pixel

    def num_lit_pixels(self):
        return sum(1 for px in self._pixels.values() if px == '#')


class Enhancer:
    def __init__(self, algorithm_line):
        self._algorithm_line = algorithm_line.strip()

    def enhance_image(self, old_image):
        code_in_background = old_image.code_in_background()
        light_background = (
            self._algorithm_line[old_image.code_in_background()] == '#')
        new_image = Image(light_background=light_background)
        xmin, xmax, ymin, ymax = old_image.borders()
        for x in range(xmin-1, xmax+2):
            for y in range(ymin-1, ymax+2):
                new_image.set_pixel(
                    x, y, self._algorithm_line[old_image.code_at_pixel(x,y)])
        return new_image


def solution(day, lines):
    enhancer = Enhancer(lines[0])
    image = Image(lines=lines[2:])
    for i in range(2):
        image = enhancer.enhance_image(image)
    print(f'Number of lit pixels after 2 enhancements: {image.num_lit_pixels()}')
    for i in range(48):
        image = enhancer.enhance_image(image)
    print(f'Number of lit pixels after 50 enhancements: {image.num_lit_pixels()}')
