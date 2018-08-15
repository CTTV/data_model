import os
# install_requires 'opentargets'
try:
    from setuptools import setup
except ImportError:
    from distutils import setup

long_description = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

setup(
    name="data_model",
    version="1.2.8",
    description=long_description.split("\n")[0],
    long_description=long_description,
    author="Gautier Koscielny",
    author_email="gautierk@targetvalidation.org",
    maintainer='Open Targets Core Team',
    maintainer_email='support@targetvalidation.org',
    url="https://github.com/opentargets/data_model",
    #packages=find_packages('.'),
    #package_dir = {'': '.'},
    #namespace_packages = ["opentargets", "opentargets.model"],
    packages=[ "opentargets","opentargets.model","opentargets.model.evidence" ],
    license="Apache 2.0",
    keywords= ['opentargets', 'bioinformatics', 'data_model'],
    classifiers=[
        "License :: Apache 2.0",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
          'iso8601>=0.1.12',
    ],
    extras_require={
          'tests': [
              'nose>=1.3.4',
              'tox>=1.7.0',
              'wheel>=0.22.0'
              ]}
)

