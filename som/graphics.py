from contextlib import contextmanager
from graphics import Circle, GraphWin, Line, Point


# drawing functionality
@contextmanager
def get_window(x=600, y=600):
    try:
        win = GraphWin('', x, y)
        yield ([], [], x, y, win)
        win.getMouse()
    finally:
        win.close()


def get_windows(n, x=600, y=600):
    wins = [([], [], x, y, GraphWin('', x, y)) for _ in range(n)]
    for win in wins:
        yield win


def draw_vecs(ctx, vec, color='red'):
    map_objs, vec_objs, w, h, win = ctx

    while vec_objs:
        vec_objs.pop().undraw()

    for v in vec:
        c = Circle(Point(v[0] * w, v[1] * h), 2)
        c.setOutline(color)
        c.setFill(color)
        vec_objs.append(c)

    for o in vec_objs:
        o.draw(win)


def draw_2d_map(ctx, m):
    map_objs, vec_objs, w, h, win = ctx

    while map_objs:
        map_objs.pop().undraw()

    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            c = Circle(Point(m[i, j, 0] * w, m[i, j, 1] * h), 5)
            c.setFill('black')
            map_objs.append(c)
            if i + 1 < m.shape[0]:
                map_objs.append(Line(
                    Point(m[i, j, 0] * w, m[i, j, 1] * h),
                    Point(m[i + 1, j, 0] * w, m[i + 1, j, 1] * h)))
            if j + 1 < m.shape[1]:
                map_objs.append(Line(
                    Point(m[i, j, 0] * w, m[i, j, 1] * h),
                    Point(m[i, j + 1, 0] * w, m[i, j + 1, 1] * h)))

    for o in map_objs:
        o.draw(win)
