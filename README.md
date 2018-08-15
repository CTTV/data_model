
# Data Model

Target-Disease evidence are represented in JSON format in Open Targets. While it's possible to 'validate' json data 
using modules such as [jsonschema](https://pypi.org/project/jsonschema/) and generate evidence strings with dictionaries 
and lists, we decided at the beginning of the project to have a python module to generate and validate evidence based on an object-oriented 
representation of the evidence. 

Hence opentargets.datamodel is a simple module to generate, validate, and compare Open Targets evidence. 
The python code is auto-generated from the json schema itself meaning that any change can be reflected immediately in the data model.

# Getting Started

The following instructions will get you a version of the module
## Installing
Using python's pip installer:
```shell
pip install git+https://github.com/opentargets/data_model.git
```
To install a specific version of the code in a specific folder, here 1.2.8:
```shell
pip install -t data_model-1.2.8 git+https://github.com/opentargets/data_model.git@1.2.8
```

## Examples

There is currently a file called test_data_model.py with examples on how to build evidence strings.
This will be updated to the latest schema to reflect the recent changes.

# Author

Gautier Koscielny

# License
Copyright 2014-2018 Biogen, Celgene Corporation, EMBL - European Bioinformatics Institute, GlaxoSmithKline, Takeda Pharmaceutical Company and Wellcome Sanger Institute

This software was developed as part of the Open Targets project. For more information please see: http://www.opentargets.org

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
