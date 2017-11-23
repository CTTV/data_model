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
import opentargets.model.evidence.core
import opentargets.model.evidence.linkout as evidence_linkout

__author__ = "Gautier Koscielny"
__copyright__ = "Copyright 2014-2017, Open Targets"
__credits__ = ["Gautier Koscielny", "Samiul Hasan"]
__license__ = "Apache 2.0"
__version__ = "1.2.7"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautierk@targetvalidation.org"
__status__ = "Production"

logger = logging.getLogger(__name__)
import opentargets.model.evidence.core as evidence_core
"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/drug/target2drug.json
"""
class Target2Drug(evidence_core.Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param evidence_codes = None
  :param mechanism_of_action = None
  :param action_type = None
  :param urls = None
  :param unique_experiment_reference = None
  :param is_associated = False
  :param date_asserted = None
  :param resource_score = None
  :param     provenance_type = None
  """
  def __init__(self, evidence_codes = None, mechanism_of_action = None, action_type = None, urls = None, unique_experiment_reference = None, is_associated = False, date_asserted = None, resource_score = None,     provenance_type = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Target2Drug, self).__init__(unique_experiment_reference = unique_experiment_reference,is_associated = is_associated,date_asserted = date_asserted,resource_score = resource_score,provenance_type = provenance_type)
    
    """
    Name: evidence_codes
    Type: array
    Description: An array of evidence codes
    Required: {True}
    """
    self.evidence_codes = evidence_codes
    
    """
    Name: mechanism_of_action
    Type: string
    Required: {True}
    """
    self.mechanism_of_action = mechanism_of_action
    
    """
    Name: action_type
    Type: string
    Required: {True}
    """
    self.action_type = action_type
    
    """
    Name: urls
    Type: array
    """
    self.urls = urls
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Target2Drug, cls).cloneObject(clone)
    if clone.evidence_codes:
        obj.evidence_codes = []; obj.evidence_codes.extend(clone.evidence_codes)
    if clone.mechanism_of_action:
        obj.mechanism_of_action = clone.mechanism_of_action
    if clone.action_type:
        obj.action_type = clone.action_type
    if clone.urls:
        obj.urls = []; obj.urls.extend(clone.urls)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['evidence_codes','mechanism_of_action','action_type','urls','unique_experiment_reference','is_associated','date_asserted','resource_score','provenance_type']
    obj = super(Target2Drug, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Target2Drug - DictType expected - {0} found\n".format(type(map)))
      return
    if  'evidence_codes' in map:
        obj.evidence_codes = map['evidence_codes']
    if  'mechanism_of_action' in map:
        obj.mechanism_of_action = map['mechanism_of_action']
    if  'action_type' in map:
        obj.action_type = map['action_type']
    if 'urls' in map and isinstance(map['urls'], list):
        obj.urls = []
        for item in map['urls']:
            obj.urls.append(evidence_linkout.Linkout.fromMap(item))
    for key in map:
      if not key in cls_keys:
        logger.warn("Target2Drug - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Target2Drug
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Target2Drug, self).validate(logger, path = path)
    if self.is_associated is None:
      logger.error("Target2Drug - {0}.is_associated is required".format(path))
      error = error + 1
    if self.date_asserted is None:
      logger.error("Target2Drug - {0}.date_asserted is required".format(path))
      error = error + 1
    if self.resource_score is None:
      logger.error("Target2Drug - {0}.resource_score is required".format(path))
      error = error + 1
    if self.provenance_type is None:
      logger.error("Target2Drug - {0}.provenance_type is required".format(path))
      error = error + 1
    # evidence_codes is mandatory
    if self.evidence_codes is None :
        logger.error("Target2Drug - {0}.evidence_codes is required".format(path))
        error = error + 1
    if not self.evidence_codes is None:
        validValues = ['http://identifiers.org/eco/target_drug','http://purl.obolibrary.org/obo/ECO_0000205']
        for item in self.evidence_codes:
            if item not in validValues:
                logger.error("Target2Drug - {0}.evidence_codes value is restricted to the fixed set of values 'http://identifiers.org/eco/target_drug','http://purl.obolibrary.org/obo/ECO_0000205' ('{1}' given)".format(path, item))
                error = error + 1
    if not self.evidence_codes is None and len(self.evidence_codes) > 0 and not all(isinstance(n, six.string_types) for n in self.evidence_codes):
        logger.error("Target2Drug - {0}.evidence_codes array should have elements of type 'six.string_types'".format(path))
        error = error+1
    if self.evidence_codes and len(self.evidence_codes) < 1:
        logger.error("Target2Drug - {0}.evidence_codes array should have at least 1 elements".format(path))
        error = error + 1
    # mechanism_of_action is mandatory
    if self.mechanism_of_action is None :
        logger.error("Target2Drug - {0}.mechanism_of_action is required".format(path))
        error = error + 1
    if self.mechanism_of_action and not isinstance(self.mechanism_of_action, six.string_types):
        logger.error("Target2Drug - {0}.mechanism_of_action type should be a string".format(path))
        error = error + 1
    # action_type is mandatory
    if self.action_type is None :
        logger.error("Target2Drug - {0}.action_type is required".format(path))
        error = error + 1
    if self.action_type and not isinstance(self.action_type, six.string_types):
        logger.error("Target2Drug - {0}.action_type type should be a string".format(path))
        error = error + 1
    if not self.urls is None and len(self.urls) > 0 and not all(isinstance(n, evidence_linkout.Linkout) for n in self.urls):
        logger.error("Target2Drug - {0}.urls array should have elements of type 'evidence_linkout.Linkout'".format(path))
        error = error+1
    return error
  
  def serialize(self):
    classDict = super(Target2Drug, self).serialize()
    if not self.evidence_codes is None: classDict['evidence_codes'] = self.evidence_codes
    if not self.mechanism_of_action is None: classDict['mechanism_of_action'] = self.mechanism_of_action
    if not self.action_type is None: classDict['action_type'] = self.action_type
    if not self.urls is None: classDict['urls'] = map(lambda x: x.serialize(), self.urls)
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
import opentargets.model.evidence.core as evidence_core
"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/drug/drug2clinic.json
"""
class Drug2Clinic(evidence_core.Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param evidence_codes = None
  :param max_phase_for_disease = None
  :param urls = None
  :param status = None
  :param unique_experiment_reference = None
  :param is_associated = False
  :param date_asserted = None
  :param resource_score = None
  :param     provenance_type = None
  """
  def __init__(self, evidence_codes = None, max_phase_for_disease = None, urls = None, status = None, unique_experiment_reference = None, is_associated = False, date_asserted = None, resource_score = None,     provenance_type = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Drug2Clinic, self).__init__(unique_experiment_reference = unique_experiment_reference,is_associated = is_associated,date_asserted = date_asserted,resource_score = resource_score,provenance_type = provenance_type)
    
    """
    Name: evidence_codes
    Type: array
    Description: An array of evidence codes
    Required: {True}
    """
    self.evidence_codes = evidence_codes
    """
    Name: max_phase_for_disease
    """
    self.max_phase_for_disease = max_phase_for_disease
    
    """
    Name: urls
    Type: array
    """
    self.urls = urls
    
    """
    Name: status
    Type: string
    """
    self.status = status
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Drug2Clinic, cls).cloneObject(clone)
    if clone.evidence_codes:
        obj.evidence_codes = []; obj.evidence_codes.extend(clone.evidence_codes)
    obj.max_phase_for_disease = Diseasephase.cloneObject(clone.max_phase_for_disease)
    if clone.urls:
        obj.urls = []; obj.urls.extend(clone.urls)
    if clone.status:
        obj.status = clone.status
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['evidence_codes','max_phase_for_disease','urls','status','unique_experiment_reference','is_associated','date_asserted','resource_score','provenance_type']
    obj = super(Drug2Clinic, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Drug2Clinic - DictType expected - {0} found\n".format(type(map)))
      return
    if  'evidence_codes' in map:
        obj.evidence_codes = map['evidence_codes']
    if  'max_phase_for_disease' in map:
        obj.max_phase_for_disease = Diseasephase.fromMap(map['max_phase_for_disease'])
    if 'urls' in map and isinstance(map['urls'], list):
        obj.urls = []
        for item in map['urls']:
            obj.urls.append(evidence_linkout.Linkout.fromMap(item))
    if  'status' in map:
        obj.status = map['status']
    for key in map:
      if not key in cls_keys:
        logger.warn("Drug2Clinic - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Drug2Clinic
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Drug2Clinic, self).validate(logger, path = path)
    if self.is_associated is None:
      logger.error("Drug2Clinic - {0}.is_associated is required".format(path))
      error = error + 1
    if self.date_asserted is None:
      logger.error("Drug2Clinic - {0}.date_asserted is required".format(path))
      error = error + 1
    if self.resource_score is None:
      logger.error("Drug2Clinic - {0}.resource_score is required".format(path))
      error = error + 1
    if self.provenance_type is None:
      logger.error("Drug2Clinic - {0}.provenance_type is required".format(path))
      error = error + 1
    # evidence_codes is mandatory
    if self.evidence_codes is None :
        logger.error("Drug2Clinic - {0}.evidence_codes is required".format(path))
        error = error + 1
    if not self.evidence_codes is None:
        validValues = ['http://identifiers.org/eco/drug_disease','http://purl.obolibrary.org/obo/ECO_0000205']
        for item in self.evidence_codes:
            if item not in validValues:
                logger.error("Drug2Clinic - {0}.evidence_codes value is restricted to the fixed set of values 'http://identifiers.org/eco/drug_disease','http://purl.obolibrary.org/obo/ECO_0000205' ('{1}' given)".format(path, item))
                error = error + 1
    if not self.evidence_codes is None and len(self.evidence_codes) > 0 and not all(isinstance(n, six.string_types) for n in self.evidence_codes):
        logger.error("Drug2Clinic - {0}.evidence_codes array should have elements of type 'six.string_types'".format(path))
        error = error+1
    if self.evidence_codes and len(self.evidence_codes) < 1:
        logger.error("Drug2Clinic - {0}.evidence_codes array should have at least 1 elements".format(path))
        error = error + 1
    if self.max_phase_for_disease is None:
        logger.error("Drug2Clinic - {0}.max_phase_for_disease is required".format(path))
        error = error + 1
    elif not isinstance(self.max_phase_for_disease, Diseasephase):
        logger.error("Diseasephase class instance expected for attribute - {0}.max_phase_for_disease".format(path))
        error = error + 1
    else:
        max_phase_for_disease_error = self.max_phase_for_disease.validate(logger, path = '.'.join([path, 'max_phase_for_disease']))
        error = error + max_phase_for_disease_error
    if not self.urls is None and len(self.urls) > 0 and not all(isinstance(n, evidence_linkout.Linkout) for n in self.urls):
        logger.error("Drug2Clinic - {0}.urls array should have elements of type 'evidence_linkout.Linkout'".format(path))
        error = error+1
    if self.status and not isinstance(self.status, six.string_types):
        logger.error("Drug2Clinic - {0}.status type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = super(Drug2Clinic, self).serialize()
    if not self.evidence_codes is None: classDict['evidence_codes'] = self.evidence_codes
    if not self.max_phase_for_disease is None: classDict['max_phase_for_disease'] = self.max_phase_for_disease.serialize()
    if not self.urls is None: classDict['urls'] = map(lambda x: x.serialize(), self.urls)
    if not self.status is None: classDict['status'] = self.status
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/drug/diseasephase.json
"""
class Diseasephase(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param numeric_index = 0
  :param label = None
  """
  def __init__(self, numeric_index = 0, label = None):
    
    """
    Name: numeric_index
    Type: number
    Description: An integer indicating the position of this study phase. Higher the number = more advanced phase.
    Required: {True}
    """
    self.numeric_index = numeric_index
    
    """
    Name: label
    Type: string
    Required: {True}
    """
    self.label = label
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.numeric_index:
        obj.numeric_index = clone.numeric_index
    if clone.label:
        obj.label = clone.label
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['numeric_index','label']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("Diseasephase - DictType expected - {0} found\n".format(type(map)))
      return
    if  'numeric_index' in map:
        obj.numeric_index = map['numeric_index']
    if  'label' in map:
        obj.label = map['label']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Diseasephase
    :returns: number of errors found during validation
    """
    error = 0
    # numeric_index is mandatory
    if self.numeric_index is None :
        logger.error("Diseasephase - {0}.numeric_index is required".format(path))
        error = error + 1
    # label is mandatory
    if self.label is None :
        logger.error("Diseasephase - {0}.label is required".format(path))
        error = error + 1
    if self.label and not isinstance(self.label, six.string_types):
        logger.error("Diseasephase - {0}.label type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = collections.OrderedDict()
    if not self.numeric_index is None: classDict['numeric_index'] = self.numeric_index
    if not self.label is None: classDict['label'] = self.label
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
