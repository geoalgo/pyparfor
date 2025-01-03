from pyparfor import parfor


def f(x, v1, v2):
    return x + v1 + v2

engines = [
    "sequential",
    "joblib",
    "futures",
    # TODO fix me in CI
    # "ray"
]

def test_empty_context():
    for engine in engines:
        res = parfor(
            f, [[1, 2, 3], [2, 2, 3], [3, 2, 3]], engine=engine
        )
        print(res)
        assert res == [6, 7, 8]


def test_list_arguments():
    for engine in engines:
        res = parfor(
            f, [[1], [2], [3]], context=dict(v1=2, v2=3), engine=engine
        )
        print(res)
        assert res == [6, 7, 8]


def test_single_argument():
    for engine in engines:
        res = parfor(
            f, [1, 2, 3], context=dict(v1=2, v2=3), engine=engine
        )
        print(res)
        assert res == [6, 7, 8]

def test_dict_arguments():
    for engine in engines:
        res = parfor(
            f, [{"x": 1}, {"x": 2}, {"x": 3}], context=dict(v1=2, v2=3), engine=engine
        )
        print(res)
        assert res == [6, 7, 8]