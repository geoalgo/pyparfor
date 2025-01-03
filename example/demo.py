from pyparfor import parfor


def f(v0: int, v1: float, v2: str) -> str:
    return f"{v0}-{v1}-{v2}"


results = parfor(
    f,
    # list of inputs to call f
    [{"v0": 1}, {"v0": 2}, {"v0": 3}],
    # context is shared across all calls of f and added the inputs, when using Ray, shared memory is used which is
    # faster if the context is large
    context=dict(v1="large-array1", v2="large-array2"),
    engine='ray',
)

# ['1-2.0-cat', '2-2.0-cat', '3-2.0-cat']
print(results)

results = parfor(
    f,
    # list of inputs to call f
    [[1], [2], [3]],
    # context is shared across all calls of f and added the inputs, when using Ray, shared memory is used which is
    # faster if the context is large
    context=dict(v1="large-array1", v2="large-array2"),
    engine='ray',
)

# ['1-2.0-cat', '2-2.0-cat', '3-2.0-cat']
print(results)
