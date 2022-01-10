import re


def solution(day, lines):
    input_re = re.compile(
        r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)")
    regions = []
    seen_outside_rectangle = False
    for line in lines:
        m = input_re.match(line)
        if not m:
            print(f'Failed to parse')
            break
        on_or_off, xmin, xmax, ymin, ymax, zmin, zmax = (
            m.group(1),
            int(m.group(2)), int(m.group(3)) + 1,
            int(m.group(4)), int(m.group(5)) + 1,
            int(m.group(6)), int(m.group(7)) + 1
        )

        if (not seen_outside_rectangle and
            (xmin < -50 or xmax > 51 or ymin < -50 or ymax > 51 or
             zmin < -50 or zmax > 51)):
                volume = sum(r.volume() for r in regions)
                print(f'Total volume in small region: {volume}')
                seen_outside_rectangle = True

        rect = Rectangle(xmin, xmax, ymin, ymax, zmin, zmax)
        for r in regions:
            r.remove_rectangle(rect)
        if on_or_off == 'on':
            regions.append(Region(rect))

    volume = sum(o.volume() for o in regions)
    print(f'Total volume: {volume}')


class Rectangle:
    """Represents a 3-dimensional rectangle and whether the cuboids in it should
    be taken as lit or unlit."""
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax, is_lit=True):
        self._xmin, self._xmax = xmin, xmax
        self._ymin, self._ymax = ymin, ymax
        self._zmin, self._zmax = zmin, zmax
        self.is_lit = is_lit

    def intersect(self, other):
        """Returns the intersection of self and other as a Rectangle.

        The intersection is taken as unlit if self is lit and vice versa, to
        facilitate volume calculation.

        If self and other do not overlap, returns None. This keeps the
        collections of overlapping rectangles from getting unwieldy."""
        xmin = max(self._xmin, other._xmin)
        xmax = min(self._xmax, other._xmax)
        ymin = max(self._ymin, other._ymin)
        ymax = min(self._ymax, other._ymax)
        zmin = max(self._zmin, other._zmin)
        zmax = min(self._zmax, other._zmax)
        if xmin >= xmax or ymin >= ymax or zmin >= zmax:
            return None
        return Rectangle(xmin, xmax, ymin, ymax, zmin, zmax, not self.is_lit)

    def volume(self):
        """Returns the total volume of self."""
        return ((self._xmax - self._xmin) *
                (self._ymax - self._ymin) *
                (self._zmax - self._zmin))


class Region:
    """Represents the part of a Rectangle that is visible through any
    overlapping rectangles.  Allows calculation of visible volume through the
    inclusion-exclusion rule."""
    def __init__(self, initial_rectangle):
        self._rectangles = [initial_rectangle]

    def remove_rectangle(self, rect):
        """Remove a new Rectangle which may occlude on the initial Rectangle."""
        overlap = self._rectangles[0].intersect(rect)
        if overlap is None:
            return

        new_rectangles = self._rectangles[:]
        new_rectangles.append(overlap)
        for r in self._rectangles[1:]:
            overlap = r.intersect(rect)
            if overlap is not None:
                new_rectangles.append(overlap)
        self._rectangles = new_rectangles

    def volume(self):
        """Returns the volume of the initial rectangle which is not occluded."""
        return sum(r.volume() if r.is_lit else -r.volume()
                   for r in self._rectangles)
