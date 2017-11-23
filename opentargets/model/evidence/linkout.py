'''
Copyright 2014-2017 EMBL - European Bioinformatics Institute, Wellcome
Trust Sanger Institute, GlaxoSmithKline and Biogen

This software was developed as part of Open Targets. For more information please see:

	http://targetvalidation.org

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import re
import sys
import iso8601
import types
import json
import logging
import six
import collections

__author__ = "Gautier Koscielny"
__copyright__ = "Copyright 2014-2017, Open Targets"
__credits__ = ["Gautier Koscielny", "Samiul Hasan"]
__license__ = "Apache 2.0"
__version__ = "1.2.7"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautierk@targetvalidation.org"
__status__ = "Production"

logger = logging.getLogger(__name__)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/linkout/linkout.json
"""
class Linkout(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param nice_name = None
  :param url = None
  """
  def __init__(self, nice_name = None, url = None):
    
    """
    Name: nice_name
    Type: string
    Required: {True}
    """
    self.nice_name = nice_name
    
    """
    Name: url
    Type: string
    Required: {True}
    String format: uri
    """
    self.url = url
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.nice_name:
        obj.nice_name = clone.nice_name
    if clone.url:
        obj.url = clone.url
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['nice_name','url']
    obj = cls()
    if not isinstance(dict_obj, types.DictType):
      logger.warn("Linkout - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'nice_name' in dict_obj:
        obj.nice_name = dict_obj['nice_name']
    if  'url' in dict_obj:
        obj.url = dict_obj['url']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Linkout
    :returns: number of errors found during validation
    """
    error = 0
    # nice_name is mandatory
    if self.nice_name is None :
        logger.error("Linkout - {0}.nice_name is required".format(path))
        error = error + 1
    if self.nice_name and not isinstance(self.nice_name, six.string_types):
        logger.error("Linkout - {0}.nice_name type should be a string".format(path))
        error = error + 1
    # url is mandatory
    if self.url is None :
        logger.error("Linkout - {0}.url is required".format(path))
        error = error + 1
    if self.url and not isinstance(self.url, six.string_types):
        logger.error("Linkout - {0}.url type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = collections.OrderedDict()
    if not self.nice_name is None: classDict['nice_name'] = self.nice_name
    if not self.url is None: classDict['url'] = self.url
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
