'''
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
__copyright__ = "Copyright 2014-2017 EMBL - European Bioinformatics Institute, Wellcome Trust Sanger Institute, GlaxoSmithKline and Biogen"
__copyright__ = "Copyright 2018 Biogen, Celgene Corporation, EMBL - European Bioinformatics Institute, GlaxoSmithKline, Takeda Pharmaceutical Company and Wellcome Sanger Institute"
__credits__ = ["Gautier Koscielny", "Samiul Hasan"]
__license__ = "Apache 2.0"
__version__ = "1.2.8"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautierk@targetvalidation.org"
__status__ = "Production"

logger = logging.getLogger(__name__)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/association_score/base.json
"""
class Base(object):
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['']
    obj = cls()
    if not isinstance(dict_obj, dict):
      logger.warn("Base - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Base
    :returns: number of errors found during validation
    """
    error = 0
    return error
  
  def serialize(self):
    classDict = collections.OrderedDict()
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/association_score/method.json
"""
class Method(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param description = None
  :param reference = None
  :param url = None
  """
  def __init__(self, description = None, reference = None, url = None):
    
    """
    Name: description
    Type: string
    Can be null: False
    """
    self.description = description
    
    """
    Name: reference
    Type: string
    Description: Note for pubmed identifiers, use the URI http://europepmc.org/abstract/MED/[0-9]+
    Can be null: False
    """
    self.reference = reference
    
    """
    Name: url
    Type: string
    Can be null: False
    String format: uri
    """
    self.url = url
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.description:
        obj.description = clone.description
    if clone.reference:
        obj.reference = clone.reference
    if clone.url:
        obj.url = clone.url
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['description','reference','url']
    obj = cls()
    if not isinstance(dict_obj, dict):
      logger.warn("Method - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'description' in dict_obj:
        obj.description = dict_obj['description']
    if  'reference' in dict_obj:
        obj.reference = dict_obj['reference']
    if  'url' in dict_obj:
        obj.url = dict_obj['url']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Method
    :returns: number of errors found during validation
    """
    error = 0
    if self.description is not None and not isinstance(self.description, six.string_types):
        logger.error("Method - {0}.description type should be a string".format(path))
        error = error + 1
    """ Check regex: http://europepmc.org/abstract/MED/[0-9]+|http://europepmc.org/articles/PMC[0-9]{4,}$ for validation"""
    if self.reference is not None and not re.match('http://europepmc.org/abstract/MED/[0-9]+|http://europepmc.org/articles/PMC[0-9]{4,}$', self.reference):
        logger.error("Method - {0}.reference '{1}'".format(path,self.reference) + " does not match pattern 'http://europepmc.org/abstract/MED/[0-9]+|http://europepmc.org/articles/PMC[0-9]{4,}$'")
        logger.warn(json.dumps(self.reference, sort_keys=True, indent=2))
    if self.reference is not None and not isinstance(self.reference, six.string_types):
        logger.error("Method - {0}.reference type should be a string".format(path))
        error = error + 1
    if self.url is not None and not isinstance(self.url, six.string_types):
        logger.error("Method - {0}.url type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = collections.OrderedDict()
    if not self.description is None: classDict['description'] = self.description
    if not self.reference is None: classDict['reference'] = self.reference
    if not self.url is None: classDict['url'] = self.url
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/association_score/probability.json
"""
class Probability(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param value = 0
  :param     method = None
  """
  def __init__(self, type = None, value = 0,     method = None):
    
    """
    Name: type
    Type: string
    Can be null: False
    Required: {True}
    """
    self.type = type
    
    """
    Name: value
    Type: number
    Can be null: False
    Required: {True}
    """
    self.value = value
    """
    Name: method
    """
    self.method = method
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Probability, cls).cloneObject(clone)
    if clone.type:
        obj.type = clone.type
    if clone.value:
        obj.value = clone.value
    if clone.method:
        obj.method = Method.cloneObject(clone.method)
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['type','value','method']
    obj = super(Probability, cls).fromDict(dict_obj)
    if not isinstance(dict_obj, dict):
      logger.warn("Probability - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'type' in dict_obj:
        obj.type = dict_obj['type']
    if  'value' in dict_obj:
        obj.value = dict_obj['value']
    if  'method' in dict_obj:
        obj.method = Method.fromDict(dict_obj['method'])
    for key in dict_obj:
      if not key in cls_keys:
        logger.warn("Probability - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Probability
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Probability, self).validate(logger, path = path)
    # type is mandatory
    if self.type is None :
        logger.error("Probability - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['probability']:
        logger.error("Probability - {0}.type value is restricted to the fixed set of values 'probability' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type is not None and not isinstance(self.type, six.string_types):
        logger.error("Probability - {0}.type type should be a string".format(path))
        error = error + 1
    # value is mandatory
    if self.value is None :
        logger.error("Probability - {0}.value is required".format(path))
        error = error + 1
    if self.value <= 0 or self.value > 1:
        logger.error("Probability - {0}.value: {1} should be greater than 0 and should be lower than or equal to 1".format(path, self.value))
        error = error+1
    if self.method:
        if not isinstance(self.method, Method):
            logger.error("Method class instance expected for attribute - {0}.method".format(path))
            error = error + 1
        else:
            method_error = self.method.validate(logger, path = '.'.join([path, 'method']))
            error = error + method_error
    return error
  
  def serialize(self):
    classDict = super(Probability, self).serialize()
    if not self.type is None: classDict['type'] = self.type
    if not self.value is None: classDict['value'] = self.value
    if not self.method is None: classDict['method'] = self.method.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/association_score/pvalue.json
"""
class Pvalue(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param value = 0
  :param     method = None
  """
  def __init__(self, type = None, value = 0,     method = None):
    
    """
    Name: type
    Type: string
    Can be null: False
    Required: {True}
    """
    self.type = type
    
    """
    Name: value
    Type: number
    Can be null: False
    Required: {True}
    """
    self.value = value
    """
    Name: method
    """
    self.method = method
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Pvalue, cls).cloneObject(clone)
    if clone.type:
        obj.type = clone.type
    if clone.value:
        obj.value = clone.value
    if clone.method:
        obj.method = Method.cloneObject(clone.method)
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['type','value','method']
    obj = super(Pvalue, cls).fromDict(dict_obj)
    if not isinstance(dict_obj, dict):
      logger.warn("Pvalue - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'type' in dict_obj:
        obj.type = dict_obj['type']
    if  'value' in dict_obj:
        obj.value = dict_obj['value']
    if  'method' in dict_obj:
        obj.method = Method.fromDict(dict_obj['method'])
    for key in dict_obj:
      if not key in cls_keys:
        logger.warn("Pvalue - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Pvalue
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Pvalue, self).validate(logger, path = path)
    # type is mandatory
    if self.type is None :
        logger.error("Pvalue - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['pvalue']:
        logger.error("Pvalue - {0}.type value is restricted to the fixed set of values 'pvalue' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type is not None and not isinstance(self.type, six.string_types):
        logger.error("Pvalue - {0}.type type should be a string".format(path))
        error = error + 1
    # value is mandatory
    if self.value is None :
        logger.error("Pvalue - {0}.value is required".format(path))
        error = error + 1
    if self.value <= 0 or self.value > 1:
        logger.error("Pvalue - {0}.value: {1} should be greater than 0 and should be lower than or equal to 1".format(path, self.value))
        error = error+1
    if self.method:
        if not isinstance(self.method, Method):
            logger.error("Method class instance expected for attribute - {0}.method".format(path))
            error = error + 1
        else:
            method_error = self.method.validate(logger, path = '.'.join([path, 'method']))
            error = error + method_error
    return error
  
  def serialize(self):
    classDict = super(Pvalue, self).serialize()
    if not self.type is None: classDict['type'] = self.type
    if not self.value is None: classDict['value'] = self.value
    if not self.method is None: classDict['method'] = self.method.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/association_score/rank.json
"""
class Rank(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param position = 0
  :param sample_size = 0
  :param     method = None
  """
  def __init__(self, type = None, position = 0, sample_size = 0,     method = None):
    
    """
    Name: type
    Type: string
    Can be null: False
    Required: {True}
    """
    self.type = type
    
    """
    Name: position
    Type: number
    Can be null: False
    Required: {True}
    """
    self.position = position
    
    """
    Name: sample_size
    Type: number
    Can be null: False
    Required: {True}
    """
    self.sample_size = sample_size
    """
    Name: method
    """
    self.method = method
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.type:
        obj.type = clone.type
    if clone.position:
        obj.position = clone.position
    if clone.sample_size:
        obj.sample_size = clone.sample_size
    if clone.method:
        obj.method = Method.cloneObject(clone.method)
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['type','position','sample_size','method']
    obj = cls()
    if not isinstance(dict_obj, dict):
      logger.warn("Rank - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'type' in dict_obj:
        obj.type = dict_obj['type']
    if  'position' in dict_obj:
        obj.position = dict_obj['position']
    if  'sample_size' in dict_obj:
        obj.sample_size = dict_obj['sample_size']
    if  'method' in dict_obj:
        obj.method = Method.fromDict(dict_obj['method'])
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Rank
    :returns: number of errors found during validation
    """
    error = 0
    # type is mandatory
    if self.type is None :
        logger.error("Rank - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['rank']:
        logger.error("Rank - {0}.type value is restricted to the fixed set of values 'rank' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type is not None and not isinstance(self.type, six.string_types):
        logger.error("Rank - {0}.type type should be a string".format(path))
        error = error + 1
    # position is mandatory
    if self.position is None :
        logger.error("Rank - {0}.position is required".format(path))
        error = error + 1
    if self.position < 1:
        logger.error("Rank - {0}.position: {1} should be greater than or equal to 1".format(path, self.position))
        error = error+1
    # sample_size is mandatory
    if self.sample_size is None :
        logger.error("Rank - {0}.sample_size is required".format(path))
        error = error + 1
    if self.sample_size < 1:
        logger.error("Rank - {0}.sample_size: {1} should be greater than or equal to 1".format(path, self.sample_size))
        error = error+1
    if self.method:
        if not isinstance(self.method, Method):
            logger.error("Method class instance expected for attribute - {0}.method".format(path))
            error = error + 1
        else:
            method_error = self.method.validate(logger, path = '.'.join([path, 'method']))
            error = error + method_error
    return error
  
  def serialize(self):
    classDict = collections.OrderedDict()
    if not self.type is None: classDict['type'] = self.type
    if not self.position is None: classDict['position'] = self.position
    if not self.sample_size is None: classDict['sample_size'] = self.sample_size
    if not self.method is None: classDict['method'] = self.method.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/association_score/summed_total.json
"""
class Summed_Total(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param value = 0
  :param     method = None
  """
  def __init__(self, type = None, value = 0,     method = None):
    
    """
    Name: type
    Type: string
    Can be null: False
    Required: {True}
    """
    self.type = type
    
    """
    Name: value
    Type: number
    Can be null: False
    Required: {True}
    """
    self.value = value
    """
    Name: method
    """
    self.method = method
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Summed_Total, cls).cloneObject(clone)
    if clone.type:
        obj.type = clone.type
    if clone.value:
        obj.value = clone.value
    if clone.method:
        obj.method = Method.cloneObject(clone.method)
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['type','value','method']
    obj = super(Summed_Total, cls).fromDict(dict_obj)
    if not isinstance(dict_obj, dict):
      logger.warn("Summed_Total - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'type' in dict_obj:
        obj.type = dict_obj['type']
    if  'value' in dict_obj:
        obj.value = dict_obj['value']
    if  'method' in dict_obj:
        obj.method = Method.fromDict(dict_obj['method'])
    for key in dict_obj:
      if not key in cls_keys:
        logger.warn("Summed_Total - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Summed_Total
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Summed_Total, self).validate(logger, path = path)
    # type is mandatory
    if self.type is None :
        logger.error("Summed_Total - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['summed_total']:
        logger.error("Summed_Total - {0}.type value is restricted to the fixed set of values 'summed_total' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type is not None and not isinstance(self.type, six.string_types):
        logger.error("Summed_Total - {0}.type type should be a string".format(path))
        error = error + 1
    # value is mandatory
    if self.value is None :
        logger.error("Summed_Total - {0}.value is required".format(path))
        error = error + 1
    if self.value <= 0:
        logger.error("Summed_Total - {0}.value: {1} should be greater than 0".format(path, self.value))
        error = error+1
    if self.method:
        if not isinstance(self.method, Method):
            logger.error("Method class instance expected for attribute - {0}.method".format(path))
            error = error + 1
        else:
            method_error = self.method.validate(logger, path = '.'.join([path, 'method']))
            error = error + method_error
    return error
  
  def serialize(self):
    classDict = super(Summed_Total, self).serialize()
    if not self.type is None: classDict['type'] = self.type
    if not self.value is None: classDict['value'] = self.value
    if not self.method is None: classDict['method'] = self.method.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
