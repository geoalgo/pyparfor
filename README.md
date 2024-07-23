# parfor

A simple implementation for embarrassingly parallel for. 
If like me you often just need an embarrassingly parallel for loop where the backend can be interchanged between
joblib, ray or just sequential execution for easy debugging.
When using Ray, one can share memory between tasks of the for loop, e.g. some context is put once in shared memory
instead of being copied over with multiprocessing/joblib.

## Installation
```
`pip install git+https://github.com/geoalgo/parfor.git`
```

## Usage

See `example/demo.py`:

```python
from parfor import parfor


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

# ['1-large-array1-large-array2', '2-large-array1-large-array2', '3-large-array1-large-array2']
print(results)
```

You can also call `parfor` by positional arguments instead of passing dictionaries:

```python
results = parfor(
    f,
    # list of inputs to call f
    [[1], [2], [3]],
    # context is shared across all calls of f and added the inputs, when using Ray, shared memory is used which is
    # faster if the context is large
    context=dict(v1="large-array1", v2="large-array2"),
    engine='ray',
)
```
This requires that the positional arguments comes before in the function `f` being called.

## Planned features
* fix Ray in CI
* Register in Pypi
