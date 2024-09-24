from tqdm import tqdm
from typing import TypeVar, Callable, List, Union

# Test ci
A = TypeVar('A')
B = TypeVar('B')


def parfor(
        f: Callable[[object], B],
        inputs: list[list | dict],
        context: dict | None = None,
        engine: str = "ray",
) -> list[B]:
    """
    Evaluates an embarrassingly parallel for-loop.
    :param f: the function to be evaluated, the function is evaluated on `f(x, **context)` for all `x` in `inputs`
    if inputs are a list and on the union of x and context keyword arguments else
    :param inputs: list of inputs to be evaluated
    :param context: additional constant arguments to be passed to `f`. When using ray, the context is put in the local
     object store which avoids serializing multiple times, when using joblib, the context is serialized for each input.
    :param engine: can be ["sequential", "ray", "joblib", "futures"]
    :return: a list where the function is evaluated on all inputs together with the context, i.e.
    `[f(x, **context) for x in inputs]`.
    """
    assert engine in ["sequential", "ray", "joblib", "futures"]
    if context is None:
        context = {}
    if engine == "sequential":
        return [
            f(**x, **context) if isinstance(x, dict) else f(*x, **context)
            for x in tqdm(inputs)
        ]
    if engine == "joblib":
        from joblib import Parallel, delayed
        return Parallel(n_jobs=-1, verbose=50)(
            delayed(f)(**x, **context) if isinstance(x, dict) else delayed(f)(*x, **context)
            for x in inputs
        )
    if engine == "futures":
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            return list(executor.map(lambda x: f(**x, **context) if isinstance(x, dict) else f(*x, **context), inputs))
    if engine == "ray":
        import ray
        if not ray.is_initialized():
            ray.init()

        @ray.remote
        def remote_f(x, context):
            return f(**x, **context) if isinstance(x, dict) else f(*x, **context)

        remote_context = ray.put(context)
        remote_results = [remote_f.remote(x, remote_context) for x in inputs]
        return [ray.get(res) for res in tqdm(remote_results)]
