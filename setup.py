#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup_requirements = [
    "pytest-runner>=5.2",
]

test_requirements = [
    "h5py>=2.10.0",
    "requests_mock>=1.11.0",
    "black>=19.10b0",
    "codecov>=2.1.4",
    "flake8>=3.8.3",
    "flake8-debugger>=3.2.1",
    "pytest>=5.4.3",
    "pytest-cov>=2.9.0",
    "pytest-raises>=0.11",
]

dev_requirements = [
    *setup_requirements,
    *test_requirements,
    "bump2version>=1.0.1",
    "coverage>=5.1",
    "ipython>=7.15.0",
    "m2r2>=0.2.7",
    "pytest-runner>=5.2",
    "Sphinx>=3.4.3, < 7.0.0",
    "sphinx_rtd_theme>=0.5.1",
    "tox>=3.15.2",
    "twine>=3.1.1",
    "wheel>=0.34.2",
]

requirements = [
    "pydantic>=1.10.11",
    "requests>=2.21.0",
    "soilgrids>=0.1.4",
    "shapely>=2.0.1",
    "pvlib>=0.10.1",
    "altair==5.0.1",
    "numpy==1.24.0",
    "aquacrop@git+https://github.com/stephansmit/aquacrop.git#61e6c49ddd98532cbee0307ffd0bb0c05428d623",
    "PyETo@git+https://github.com/stephansmit/PyETo.git#79ddd88d727c7ebdad0ce26e220528d2921b66ea"
    "pvpumpingsystem@git+https://github.com/stephansmit/pvpumpingsystem.git#4bc78e1f75beca84a884633e1d8af1172980609b"
]

extra_requirements = {
    "setup": setup_requirements,
    "test": test_requirements,
    "dev": dev_requirements,
    "all": [
        *requirements,
        *dev_requirements,
    ]
}

setup(
    author="Stephan Smit",
    author_email="stephansmit@hotmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="This package contains all the code required for the heliostrome application",
    entry_points={
        "console_scripts": [
            "my_example=heliostrome.bin.my_example:main"
        ],
    },
    install_requires=requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="heliostrome",
    name="heliostrome",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*"]),
    python_requires=">=3.7",
    setup_requires=setup_requirements,
    test_suite="heliostrome/tests",
    tests_require=test_requirements,
    extras_require=extra_requirements,
    url="https://github.com/stephansmit/heliostrome",
    # Do not edit this string manually, always use bumpversion
    # Details in CONTRIBUTING.rst
    version="0.1.0",
    zip_safe=False,
)
