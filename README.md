# parfor

A simple implementation for embarrassingly parallel for. 
It supports the following backends: native multiprocessing, joblib and ray.
When using Ray, one can simply share memory between tasks of the for loop.

## Installation
```
pip install git+https://github.com/geoalgo/parfor.git
```

## Usage
See test `tst/test_parfor.py` for now.

## Planned features
* CI
* Documentation
* Register in Pypi
