from setuptools import setup, find_packages

extras_require = {
    "joblib": ["joblib"],
    "ray": ["ray"],
    "dev": ["pytest"],
}
all_reqs = []
for k, v in extras_require.items():
    all_reqs += v
extras_require["all"] = all_reqs

setup(
    name='pyparfor',
    version='0.0.1',
    packages=find_packages(exclude='tst'),
    url='https://github.com/geoalgo/pyparfor',
    license='Apache-2.0',
    author='Geoalgo',
    install_requires=["tqdm"],  # TODO consider making optional
    extras_require=extras_require,
    description='A simple implementation for embarrassingly parallel for supporting multiple backends.',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
)
