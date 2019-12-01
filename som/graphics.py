from contextlib import contextmanager
from graphics import Circle, GraphWin, Line, Point


# drawing functionality
@contextmanager
def get_window(x=600, y=600):
    try:
        win = GraphWin('', x, y)
        yield ([], x, y, win)
        win.getMouse()
    finally:
        win.close()


def draw_2d_map(ctx, m, vec):
    draw_objs, w, h, win = ctx

    while draw_objs:
        draw_objs.pop().undraw()

    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            c = Circle(Point(m[i, j, 0] * w, m[i, j, 1] * h), 5)
            c.setFill('black')
            draw_objs.append(c)
            if i + 1 < m.shape[0]:
                draw_objs.append(Line(
                    Point(m[i, j, 0] * w, m[i, j, 1] * h),
                    Point(m[i + 1, j, 0] * w, m[i + 1, j, 1] * h)))
            if j + 1 < m.shape[1]:
                draw_objs.append(Line(
                    Point(m[i, j, 0] * w, m[i, j, 1] * h),
                    Point(m[i, j + 1, 0] * w, m[i, j + 1, 1] * h)))

    for v in vec:
        c = Circle(Point(v[0] * w, v[1] * h), 2)
        c.setOutline('red')
        c.setFill('red')
        draw_objs.append(c)

    for o in draw_objs:
        o.draw(win)
