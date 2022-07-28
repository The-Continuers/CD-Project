import functools


def compose2(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose_list(*fs):
    return functools.reduce(compose2, fs)


def test():
    res = compose_list(lambda a: -a,
                       lambda a, b: a * b
                       )(2, 3)
    assert res == -6
