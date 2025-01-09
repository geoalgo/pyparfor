from collections.abc import Iterable
from typing import TypeVar, Callable

from tqdm import tqdm

# Test ci
A = TypeVar('A')
B = TypeVar('B')


def parfor(
        f: Callable[[object], B],
        inputs: list[object | list | dict],
        context: dict | None = None,
        engine: str = "ray",
        max_workers: int | None = None,
) -> list[B]:
    """
    Evaluates an embarrassingly parallel for-loop.
    :param f: the function to be evaluated, the function is evaluated on `f(x, **context)` for all `x` in `inputs`
    if inputs are a list and on the union of x and context keyword arguments else
    :param inputs: list of inputs to be evaluated, must be list of arguments or keyword arguments or list of
    single argument.
    :param context: additional constant arguments to be passed to `f`. When using ray, the context is put in the local
     object store which avoids serializing multiple times, when using joblib, the context is serialized for each input.
    :param engine: can be ["sequential", "ray", "joblib", "futures"]
    :param max_workers: number of workers to be used
    :return: a list where the function is evaluated on all inputs together with the context, i.e.
    `[f(x, **context) for x in inputs]`.
    """
    assert engine in ["sequential", "ray", "joblib", "futures"]
    if len(inputs) == 0:
        return []

    first_input = next(iter(inputs))
    if not isinstance(first_input, Iterable):
        # make input as list to be passed as non keyword arguments
        inputs = [[x] for x in inputs]

    if context is None:
        context = {}
    if engine == "sequential":
        return [
            f(**x, **context) if isinstance(x, dict) else f(*x, **context)
            for x in tqdm(inputs)
        ]
    if engine == "joblib":
        from joblib import Parallel, delayed
        n_jobs = -1 if max_workers is None else max_workers
        return Parallel(n_jobs=n_jobs, verbose=50)(
            delayed(f)(**x, **context) if isinstance(x, dict) else delayed(f)(*x, **context)
            for x in inputs
        )
    if engine == "futures":
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            return list(tqdm(
                executor.map(lambda x: f(**x, **context) if isinstance(x, dict) else f(*x, **context), inputs),
                total=len(inputs),
            ))
    if engine == "ray":
        import ray
        if not ray.is_initialized():
            # TODO name gap
            ray.init(num_cpus=max_workers)

        @ray.remote
        def remote_f(x, context):
            return f(**x, **context) if isinstance(x, dict) else f(*x, **context)

        remote_context = ray.put(context)
        remote_results = [remote_f.remote(x, remote_context) for x in inputs]
        return [ray.get(res) for res in tqdm(remote_results)]
