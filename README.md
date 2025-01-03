# PyParFor

PyParFor is a wrapper to perform embarrassingly parallel for loops in Python. 
It allows to switch the backend easily between sequential (for debugging), multiprocessing (with joblib), ray (to share memory) or futures.
When using Ray, one can share memory between tasks of the for loop, e.g. some context is put once in shared memory instead of being copied over with multiprocessing/joblib.


## Usage

Here is an example on how to use `PyParFor` in python, you can also check the example in `example/demo.py`:

```python
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
    engine='ray',  # can be 'sequential', 'joblib', 'futures', 'ray'
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

## Choosing the backend

Here is a potential use-case for each of the backend:
* `sequential`: great for debugging
* `futures`: great for distributing many operations that are IO bound and not compute bound. For instance, querying an
  external API is a good use-case, parallelizing matrix computation is a bad one.
* `joblib`: great for distributing many operations that are compute bound. For instance, parallelizing matrix 
computation where little context needs to be shared between tasks.
* `ray`: great for distributing many operations that are compute bound where large context needs to be shared between
  tasks (for instance sharing a large array, a large object, ...). When using Ray, one can share memory between tasks
  of the for loop, e.g. some context is put once in shared memory instead of being copied over with 
multiprocessing/joblib. The biggest drawbacks of using Ray are that it requires a large time to initialize and
Ray has a large amount of dependencies.

## Installation
```
pip install git+https://github.com/geoalgo/pyparfor.git
```

## Planned features
* fix Ray in CI
* Register in Pypi if no better alternative (best one found so far is https://github.com/fergalm/parmap we could merge ray backend ideally)

