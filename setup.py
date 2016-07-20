import os

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

long_description = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(
    name="data_model",
    version="1.2.3",
    description=long_description.split("\n")[0],
    long_description=long_description,
    author="Gautier Koscielny",
    author_email="gautierk@targetvalidation.org",
    url="https://github.com/CTTV/data_model",
    #packages=find_packages('.'),
    #package_dir = {'': '.'},
    #namespace_packages = ["opentargets", "opentargets.model"],
    packages=[ "opentargets","opentargets.model","opentargets.model.evidence" ],
    license="Apache2",
    classifiers=[
        "License :: Apache 2",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)

