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
import opentargets.model.evidence.drug as evidence_drug

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
https://raw.githubusercontent.com/opentargets/json_schema/master/src/bioentity/base.json
"""
class Base(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param id = None
  """
  def __init__(self, id = None):
    
    """
    Name: id
    Type: string
    Can be null: False
    """
    self.id = id
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.id:
        obj.id = clone.id
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['id']
    obj = cls()
    if not isinstance(dict_obj, dict):
      logger.warn("Base - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'id' in dict_obj:
        obj.id = dict_obj['id']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Base
    :returns: number of errors found during validation
    """
    error = 0
    if self.id is not None and not isinstance(self.id, six.string_types):
        logger.error("Base - {0}.id type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = collections.OrderedDict()
    if not self.id is None: classDict['id'] = self.id
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/bioentity/disease.json
"""
class Disease(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param name = None
  :param source_name = None
  :param     biosample = None
  :param id = None
  """
  def __init__(self, name = None, source_name = None,     biosample = None, id = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Disease, self).__init__(id = id)
    
    """
    Name: id
    Type: string
    Description: A valid EFO IRI
    Can be null: False
    Required: {True}
    """
    self.id = id
    
    """
    Name: name
    Type: string
    Description: Optional - EFO disease name corresponding to the EFO ID
    Can be null: False
    """
    self.name = name
    
    """
    Name: source_name
    Type: string
    Description: Optional - EFO disease name corresponding to the EFO ID
    Can be null: False
    """
    self.source_name = source_name
    """
    Name: biosample
    """
    self.biosample = biosample
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Disease, cls).cloneObject(clone)
    if clone.id:
        obj.id = clone.id
    if clone.name:
        obj.name = clone.name
    if clone.source_name:
        obj.source_name = clone.source_name
    if clone.biosample:
        obj.biosample = DiseaseBiosample.cloneObject(clone.biosample)
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['id','name','source_name','biosample','id']
    obj = super(Disease, cls).fromDict(dict_obj)
    if not isinstance(dict_obj, dict):
      logger.warn("Disease - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'id' in dict_obj:
        obj.id = dict_obj['id']
    if  'name' in dict_obj:
        obj.name = dict_obj['name']
    if  'source_name' in dict_obj:
        obj.source_name = dict_obj['source_name']
    if  'biosample' in dict_obj:
        obj.biosample = DiseaseBiosample.fromDict(dict_obj['biosample'])
    for key in dict_obj:
      if not key in cls_keys:
        logger.warn("Disease - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Disease
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Disease, self).validate(logger, path = path)
    if self.id is None:
      logger.error("Disease - {0}.id is required".format(path))
      error = error + 1
    # id is mandatory
    if self.id is None :
        logger.error("Disease - {0}.id is required".format(path))
        error = error + 1
    """ Check regex: ^http://purl.bioontology.org/omim/OMIM_[0-9]{1,}|http://www.orpha.net/ORDO/Orphanet_[0-9]{1,}|http://purl.obolibrary.org/obo/DOID_[0-9]{2,}|http://www.ebi.ac.uk/efo/EFO_[0-9]{7,}|http://purl.obolibrary.org/obo/HP_[0-9]{4,}|http://purl.obolibrary.org/obo/GO_[0-9]{4,}|http://purl.obolibrary.org/obo/MP_[0-9]{3,}|http://purl.obolibrary.org/obo/MPATH_[0-9]{3,}$ for validation"""
    if self.id is not None and not re.match('^http://purl.bioontology.org/omim/OMIM_[0-9]{1,}|http://www.orpha.net/ORDO/Orphanet_[0-9]{1,}|http://purl.obolibrary.org/obo/DOID_[0-9]{2,}|http://www.ebi.ac.uk/efo/EFO_[0-9]{7,}|http://purl.obolibrary.org/obo/HP_[0-9]{4,}|http://purl.obolibrary.org/obo/GO_[0-9]{4,}|http://purl.obolibrary.org/obo/MP_[0-9]{3,}|http://purl.obolibrary.org/obo/MPATH_[0-9]{3,}$', self.id):
        logger.error("Disease - {0}.id '{1}'".format(path,self.id) + " does not match pattern '^http://purl.bioontology.org/omim/OMIM_[0-9]{1,}|http://www.orpha.net/ORDO/Orphanet_[0-9]{1,}|http://purl.obolibrary.org/obo/DOID_[0-9]{2,}|http://www.ebi.ac.uk/efo/EFO_[0-9]{7,}|http://purl.obolibrary.org/obo/HP_[0-9]{4,}|http://purl.obolibrary.org/obo/GO_[0-9]{4,}|http://purl.obolibrary.org/obo/MP_[0-9]{3,}|http://purl.obolibrary.org/obo/MPATH_[0-9]{3,}$'")
        logger.warn(json.dumps(self.id, sort_keys=True, indent=2))
    if self.id is not None and not isinstance(self.id, six.string_types):
        logger.error("Disease - {0}.id type should be a string".format(path))
        error = error + 1
    if self.name is not None and not isinstance(self.name, six.string_types):
        logger.error("Disease - {0}.name type should be a string".format(path))
        error = error + 1
    if self.source_name is not None and not isinstance(self.source_name, six.string_types):
        logger.error("Disease - {0}.source_name type should be a string".format(path))
        error = error + 1
    if self.biosample:
        if not isinstance(self.biosample, DiseaseBiosample):
            logger.error("DiseaseBiosample class instance expected for attribute - {0}.biosample".format(path))
            error = error + 1
        else:
            biosample_error = self.biosample.validate(logger, path = '.'.join([path, 'biosample']))
            error = error + biosample_error
    return error
  
  def serialize(self):
    classDict = super(Disease, self).serialize()
    if not self.id is None: classDict['id'] = self.id
    if not self.name is None: classDict['name'] = self.name
    if not self.source_name is None: classDict['source_name'] = self.source_name
    if not self.biosample is None: classDict['biosample'] = self.biosample.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/bioentity/disease.json inner class:(biosample)
"""
class DiseaseBiosample(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param name = None
  :param id = None
  """
  def __init__(self, name = None, id = None):
    
    """
    Name: name
    Type: string
    Description: free text of the tissue / cell name
    Can be null: False
    Required: {True}
    """
    self.name = name
    
    """
    Name: id
    Type: string
    Description: EFO ID of the tissue - optional
    Can be null: False
    String format: uri
    """
    self.id = id
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.name:
        obj.name = clone.name
    if clone.id:
        obj.id = clone.id
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['name','id']
    obj = cls()
    if not isinstance(dict_obj, dict):
      logger.warn("DiseaseBiosample - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'name' in dict_obj:
        obj.name = dict_obj['name']
    if  'id' in dict_obj:
        obj.id = dict_obj['id']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class DiseaseBiosample
    :returns: number of errors found during validation
    """
    error = 0
    # name is mandatory
    if self.name is None :
        logger.error("DiseaseBiosample - {0}.name is required".format(path))
        error = error + 1
    if self.name is not None and not isinstance(self.name, six.string_types):
        logger.error("DiseaseBiosample - {0}.name type should be a string".format(path))
        error = error + 1
    if self.id is not None and not isinstance(self.id, six.string_types):
        logger.error("DiseaseBiosample - {0}.id type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = collections.OrderedDict()
    if not self.name is None: classDict['name'] = self.name
    if not self.id is None: classDict['id'] = self.id
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/bioentity/target.json
"""
class Target(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param tier = None
  :param complex_id = None
  :param complex_members = None
  :param complex_type = None
  :param target_type = None
  :param activity = None
  :param target_name = None
  :param target_class = None
  :param id = None
  """
  def __init__(self, tier = None, complex_id = None, complex_members = None, complex_type = None, target_type = None, activity = None, target_name = None, target_class = None, id = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Target, self).__init__(id = id)
    
    """
    Name: id
    Type: string
    Description: An Ensembl or UniProt identifier
    Can be null: False
    Required: {True}
    """
    self.id = id
    
    """
    Name: tier
    Type: string
    Description: Cancer Gene Census genes has been split into two tiers
    Can be null: False
    """
    self.tier = tier
    
    """
    Name: complex_id
    Type: string
    Description: A ChEMBL protein complex identifier
    Can be null: False
    """
    self.complex_id = complex_id
    
    """
    Name: complex_members
    Type: array
    Can be null: False
    """
    self.complex_members = complex_members
    
    """
    Name: complex_type
    Type: string
    Description: Type of target
    Can be null: False
    """
    self.complex_type = complex_type
    
    """
    Name: target_type
    Type: string
    Description: Type of target; if you do not have detailed information, select from gene_evidence, protein_evidence or transcript_evidence
    Can be null: False
    Required: {True}
    """
    self.target_type = target_type
    
    """
    Name: activity
    Type: string
    Description: Activity of target in disease context
    Can be null: False
    Required: {True}
    """
    self.activity = activity
    
    """
    Name: target_name
    Type: string
    Description: used by ChEMBL initially if they have a more canonical target name, optional
    Can be null: False
    """
    self.target_name = target_name
    
    """
    Name: target_class
    Type: array
    Can be null: False
    """
    self.target_class = target_class
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Target, cls).cloneObject(clone)
    if clone.id:
        obj.id = clone.id
    if clone.tier:
        obj.tier = clone.tier
    if clone.complex_id:
        obj.complex_id = clone.complex_id
    if clone.complex_members:
        obj.complex_members = list(); obj.complex_members.extend(clone.complex_members)
    if clone.complex_type:
        obj.complex_type = clone.complex_type
    if clone.target_type:
        obj.target_type = clone.target_type
    if clone.activity:
        obj.activity = clone.activity
    if clone.target_name:
        obj.target_name = clone.target_name
    if clone.target_class:
        obj.target_class = list(); obj.target_class.extend(clone.target_class)
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['id','tier','complex_id','complex_members','complex_type','target_type','activity','target_name','target_class','id']
    obj = super(Target, cls).fromDict(dict_obj)
    if not isinstance(dict_obj, dict):
      logger.warn("Target - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'id' in dict_obj:
        obj.id = dict_obj['id']
    if  'tier' in dict_obj:
        obj.tier = dict_obj['tier']
    if  'complex_id' in dict_obj:
        obj.complex_id = dict_obj['complex_id']
    if  'complex_members' in dict_obj:
        obj.complex_members = dict_obj['complex_members']
    if  'complex_type' in dict_obj:
        obj.complex_type = dict_obj['complex_type']
    if  'target_type' in dict_obj:
        obj.target_type = dict_obj['target_type']
    if  'activity' in dict_obj:
        obj.activity = dict_obj['activity']
    if  'target_name' in dict_obj:
        obj.target_name = dict_obj['target_name']
    if  'target_class' in dict_obj:
        obj.target_class = dict_obj['target_class']
    for key in dict_obj:
      if not key in cls_keys:
        logger.warn("Target - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Target
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Target, self).validate(logger, path = path)
    if self.id is None:
      logger.error("Target - {0}.id is required".format(path))
      error = error + 1
    # id is mandatory
    if self.id is None :
        logger.error("Target - {0}.id is required".format(path))
        error = error + 1
    """ Check regex: ^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$ for validation"""
    if self.id is not None and not re.match('^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$', self.id):
        logger.error("Target - {0}.id '{1}'".format(path,self.id) + " does not match pattern '^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$'")
        logger.warn(json.dumps(self.id, sort_keys=True, indent=2))
    if self.id is not None and not isinstance(self.id, six.string_types):
        logger.error("Target - {0}.id type should be a string".format(path))
        error = error + 1
    if not self.tier is None and not self.tier in ['tier 1','tier 2']:
        logger.error("Target - {0}.tier value is restricted to the fixed set of values 'tier 1','tier 2' ('{1}' given)".format(path, self.tier))
        error = error + 1
    if self.tier is not None and not isinstance(self.tier, six.string_types):
        logger.error("Target - {0}.tier type should be a string".format(path))
        error = error + 1
    """ Check regex: ^CHEMBL[0-9]+$ for validation"""
    if self.complex_id is not None and not re.match('^CHEMBL[0-9]+$', self.complex_id):
        logger.error("Target - {0}.complex_id '{1}'".format(path,self.complex_id) + " does not match pattern '^CHEMBL[0-9]+$'")
        logger.warn(json.dumps(self.complex_id, sort_keys=True, indent=2))
    if self.complex_id is not None and not isinstance(self.complex_id, six.string_types):
        logger.error("Target - {0}.complex_id type should be a string".format(path))
        error = error + 1
    if self.complex_members is not None and len(self.complex_members) > 0 and not all(isinstance(n, six.string_types) for n in self.complex_members):
        logger.error("Target - {0}.complex_members array should have elements of type 'six.string_types'".format(path))
        error = error+1
    if self.complex_members is not None and len(self.complex_members) < 1:
        logger.error("Target - {0}.complex_members array should have at least 1 elements".format(path))
        error = error + 1
    if self.complex_members is not None and len(set(self.complex_members)) != len(self.complex_members):
        logger.error("Target - {0}.complex_members array have duplicated elements".format(path))
        error = error + 1
    """ Check regex: ^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$ for validation of array item"""
    if self.complex_members is not None and len(self.complex_members) > 0 and not all(re.match('^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$', n) for n in self.complex_members):
        logger.error("Target - {0}.complex_members items".format(path) + " do not match pattern '^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$'")
    if not self.complex_type is None and not self.complex_type in ['http://identifiers.org/cttv.target/chimeric_protein','http://identifiers.org/cttv.target/protein_complex','http://identifiers.org/cttv.target/protein_complex_group','http://identifiers.org/cttv.target/protein_complex_heteropolymer','http://identifiers.org/cttv.target/protein_complex_homopolymer','http://identifiers.org/cttv.target/protein_family','http://identifiers.org/cttv.target/selectivity_group']:
        logger.error("Target - {0}.complex_type value is restricted to the fixed set of values 'http://identifiers.org/cttv.target/chimeric_protein','http://identifiers.org/cttv.target/protein_complex','http://identifiers.org/cttv.target/protein_complex_group','http://identifiers.org/cttv.target/protein_complex_heteropolymer','http://identifiers.org/cttv.target/protein_complex_homopolymer','http://identifiers.org/cttv.target/protein_family','http://identifiers.org/cttv.target/selectivity_group' ('{1}' given)".format(path, self.complex_type))
        error = error + 1
    if self.complex_type is not None and not isinstance(self.complex_type, six.string_types):
        logger.error("Target - {0}.complex_type type should be a string".format(path))
        error = error + 1
    # target_type is mandatory
    if self.target_type is None :
        logger.error("Target - {0}.target_type is required".format(path))
        error = error + 1
    if not self.target_type is None and not self.target_type in ['http://identifiers.org/cttv.target/gene_allele','http://identifiers.org/cttv.target/gene_evidence','http://identifiers.org/cttv.target/gene_in_LD_region','http://identifiers.org/cttv.target/gene_in_epigenetic_regulation_complex','http://identifiers.org/cttv.target/gene_variant','http://identifiers.org/cttv.target/pro_protein','http://identifiers.org/cttv.target/protein_evidence','http://identifiers.org/cttv.target/transcript_evidence','http://identifiers.org/cttv.target/transcript_isoform','http://identifiers.org/cttv.target/protein_isoform','http://identifiers.org/cttv.target/gene_or_protein_or_transcript']:
        logger.error("Target - {0}.target_type value is restricted to the fixed set of values 'http://identifiers.org/cttv.target/gene_allele','http://identifiers.org/cttv.target/gene_evidence','http://identifiers.org/cttv.target/gene_in_LD_region','http://identifiers.org/cttv.target/gene_in_epigenetic_regulation_complex','http://identifiers.org/cttv.target/gene_variant','http://identifiers.org/cttv.target/pro_protein','http://identifiers.org/cttv.target/protein_evidence','http://identifiers.org/cttv.target/transcript_evidence','http://identifiers.org/cttv.target/transcript_isoform','http://identifiers.org/cttv.target/protein_isoform','http://identifiers.org/cttv.target/gene_or_protein_or_transcript' ('{1}' given)".format(path, self.target_type))
        error = error + 1
    if self.target_type is not None and not isinstance(self.target_type, six.string_types):
        logger.error("Target - {0}.target_type type should be a string".format(path))
        error = error + 1
    # activity is mandatory
    if self.activity is None :
        logger.error("Target - {0}.activity is required".format(path))
        error = error + 1
    if not self.activity is None and not self.activity in ['http://identifiers.org/cttv.activity/decreased_transcript_level','http://identifiers.org/cttv.activity/decreased_translational_product_level','http://identifiers.org/cttv.activity/drug_negative_modulator','http://identifiers.org/cttv.activity/drug_positive_modulator','http://identifiers.org/cttv.activity/gain_of_function','http://identifiers.org/cttv.activity/increased_transcript_level','http://identifiers.org/cttv.activity/increased_translational_product_level','http://identifiers.org/cttv.activity/loss_of_function','http://identifiers.org/cttv.activity/partial_loss_of_function','http://identifiers.org/cttv.activity/up_or_down','http://identifiers.org/cttv.activity/up','http://identifiers.org/cttv.activity/down','http://identifiers.org/cttv.activity/tolerated','http://identifiers.org/cttv.activity/predicted','http://identifiers.org/cttv.activity/damaging','http://identifiers.org/cttv.activity/damaging_to_target','http://identifiers.org/cttv.activity/predicted_tolerated','http://identifiers.org/cttv.activity/predicted_damaging','http://identifiers.org/cttv.activity/tolerated_by_target','http://identifiers.org/cttv.activity/unknown']:
        logger.error("Target - {0}.activity value is restricted to the fixed set of values 'http://identifiers.org/cttv.activity/decreased_transcript_level','http://identifiers.org/cttv.activity/decreased_translational_product_level','http://identifiers.org/cttv.activity/drug_negative_modulator','http://identifiers.org/cttv.activity/drug_positive_modulator','http://identifiers.org/cttv.activity/gain_of_function','http://identifiers.org/cttv.activity/increased_transcript_level','http://identifiers.org/cttv.activity/increased_translational_product_level','http://identifiers.org/cttv.activity/loss_of_function','http://identifiers.org/cttv.activity/partial_loss_of_function','http://identifiers.org/cttv.activity/up_or_down','http://identifiers.org/cttv.activity/up','http://identifiers.org/cttv.activity/down','http://identifiers.org/cttv.activity/tolerated','http://identifiers.org/cttv.activity/predicted','http://identifiers.org/cttv.activity/damaging','http://identifiers.org/cttv.activity/damaging_to_target','http://identifiers.org/cttv.activity/predicted_tolerated','http://identifiers.org/cttv.activity/predicted_damaging','http://identifiers.org/cttv.activity/tolerated_by_target','http://identifiers.org/cttv.activity/unknown' ('{1}' given)".format(path, self.activity))
        error = error + 1
    if self.activity is not None and not isinstance(self.activity, six.string_types):
        logger.error("Target - {0}.activity type should be a string".format(path))
        error = error + 1
    if self.target_name is not None and not isinstance(self.target_name, six.string_types):
        logger.error("Target - {0}.target_name type should be a string".format(path))
        error = error + 1
    if self.target_class is not None and len(self.target_class) > 0 and not all(isinstance(n, six.string_types) for n in self.target_class):
        logger.error("Target - {0}.target_class array should have elements of type 'six.string_types'".format(path))
        error = error+1
    return error
  
  def serialize(self):
    classDict = super(Target, self).serialize()
    if not self.id is None: classDict['id'] = self.id
    if not self.tier is None: classDict['tier'] = self.tier
    if not self.complex_id is None: classDict['complex_id'] = self.complex_id
    if not self.complex_members is None: classDict['complex_members'] = self.complex_members
    if not self.complex_type is None: classDict['complex_type'] = self.complex_type
    if not self.target_type is None: classDict['target_type'] = self.target_type
    if not self.activity is None: classDict['activity'] = self.activity
    if not self.target_name is None: classDict['target_name'] = self.target_name
    if not self.target_class is None: classDict['target_class'] = self.target_class
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/bioentity/phenotype.json
"""
class Phenotype(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param term_id = None
  :param label = None
  :param species = None
  :param id = None
  """
  def __init__(self, term_id = None, label = None, species = None, id = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Phenotype, self).__init__(id = id)
    
    """
    Name: term_id
    Type: string
    Description: Phenotype term Identifier from HPO/MP
    Can be null: False
    Required: {True}
    """
    self.term_id = term_id
    
    """
    Name: label
    Type: string
    Description: Phenotype term label
    Can be null: False
    Required: {True}
    """
    self.label = label
    
    """
    Name: species
    Type: string
    Can be null: False
    Required: {True}
    """
    self.species = species
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Phenotype, cls).cloneObject(clone)
    if clone.term_id:
        obj.term_id = clone.term_id
    if clone.label:
        obj.label = clone.label
    if clone.species:
        obj.species = clone.species
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['term_id','label','species','id']
    obj = super(Phenotype, cls).fromDict(dict_obj)
    if not isinstance(dict_obj, dict):
      logger.warn("Phenotype - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'term_id' in dict_obj:
        obj.term_id = dict_obj['term_id']
    if  'label' in dict_obj:
        obj.label = dict_obj['label']
    if  'species' in dict_obj:
        obj.species = dict_obj['species']
    for key in dict_obj:
      if not key in cls_keys:
        logger.warn("Phenotype - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Phenotype
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Phenotype, self).validate(logger, path = path)
    if self.id is None:
      logger.error("Phenotype - {0}.id is required".format(path))
      error = error + 1
    # term_id is mandatory
    if self.term_id is None :
        logger.error("Phenotype - {0}.term_id is required".format(path))
        error = error + 1
    """ Check regex: ^http://purl.obolibrary.org/obo/HP_[0-9]{4,}||http://purl.obolibrary.org/obo/MP_[0-9]{4,}$ for validation"""
    if self.term_id is not None and not re.match('^http://purl.obolibrary.org/obo/HP_[0-9]{4,}||http://purl.obolibrary.org/obo/MP_[0-9]{4,}$', self.term_id):
        logger.error("Phenotype - {0}.term_id '{1}'".format(path,self.term_id) + " does not match pattern '^http://purl.obolibrary.org/obo/HP_[0-9]{4,}||http://purl.obolibrary.org/obo/MP_[0-9]{4,}$'")
        logger.warn(json.dumps(self.term_id, sort_keys=True, indent=2))
    if self.term_id is not None and not isinstance(self.term_id, six.string_types):
        logger.error("Phenotype - {0}.term_id type should be a string".format(path))
        error = error + 1
    # label is mandatory
    if self.label is None :
        logger.error("Phenotype - {0}.label is required".format(path))
        error = error + 1
    if self.label is not None and not isinstance(self.label, six.string_types):
        logger.error("Phenotype - {0}.label type should be a string".format(path))
        error = error + 1
    # species is mandatory
    if self.species is None :
        logger.error("Phenotype - {0}.species is required".format(path))
        error = error + 1
    if not self.species is None and not self.species in ['mouse','human','rat','zebrafish','dog']:
        logger.error("Phenotype - {0}.species value is restricted to the fixed set of values 'mouse','human','rat','zebrafish','dog' ('{1}' given)".format(path, self.species))
        error = error + 1
    if self.species is not None and not isinstance(self.species, six.string_types):
        logger.error("Phenotype - {0}.species type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = super(Phenotype, self).serialize()
    if not self.term_id is None: classDict['term_id'] = self.term_id
    if not self.label is None: classDict['label'] = self.label
    if not self.species is None: classDict['species'] = self.species
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/bioentity/drug.json
"""
class Drug(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param molecule_name = None
  :param molecule_type = None
  :param     max_phase_for_all_diseases = None
  :param withdrawn_country = None
  :param withdrawn_reason = None
  :param withdrawn_year = None
  :param id = None
  """
  def __init__(self, molecule_name = None, molecule_type = None,     max_phase_for_all_diseases = None, withdrawn_country = None, withdrawn_reason = None, withdrawn_year = None, id = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Drug, self).__init__(id = id)
    
    """
    Name: id
    Type: string
    Description: A ChEMBL or internal drug identifier
    Can be null: False
    Required: {True}
    """
    self.id = id
    
    """
    Name: molecule_name
    Type: string
    Can be null: False
    Required: {True}
    """
    self.molecule_name = molecule_name
    
    """
    Name: molecule_type
    Type: string
    Can be null: False
    Required: {True}
    """
    self.molecule_type = molecule_type
    """
    Name: max_phase_for_all_diseases
    """
    self.max_phase_for_all_diseases = max_phase_for_all_diseases
    
    """
    Name: withdrawn_country
    Type: string
    Can be null: True
    """
    self.withdrawn_country = withdrawn_country
    
    """
    Name: withdrawn_reason
    Type: string
    Can be null: True
    """
    self.withdrawn_reason = withdrawn_reason
    
    """
    Name: withdrawn_year
    Type: string
    Can be null: True
    """
    self.withdrawn_year = withdrawn_year
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Drug, cls).cloneObject(clone)
    if clone.id:
        obj.id = clone.id
    if clone.molecule_name:
        obj.molecule_name = clone.molecule_name
    if clone.molecule_type:
        obj.molecule_type = clone.molecule_type
    if clone.max_phase_for_all_diseases:
        obj.max_phase_for_all_diseases = evidence_drug.Diseasephase.cloneObject(clone.max_phase_for_all_diseases)
    if clone.withdrawn_country:
        obj.withdrawn_country = clone.withdrawn_country
    if clone.withdrawn_reason:
        obj.withdrawn_reason = clone.withdrawn_reason
    if clone.withdrawn_year:
        obj.withdrawn_year = clone.withdrawn_year
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['id','molecule_name','molecule_type','max_phase_for_all_diseases','withdrawn_country','withdrawn_reason','withdrawn_year','id']
    obj = super(Drug, cls).fromDict(dict_obj)
    if not isinstance(dict_obj, dict):
      logger.warn("Drug - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'id' in dict_obj:
        obj.id = dict_obj['id']
    if  'molecule_name' in dict_obj:
        obj.molecule_name = dict_obj['molecule_name']
    if  'molecule_type' in dict_obj:
        obj.molecule_type = dict_obj['molecule_type']
    if  'max_phase_for_all_diseases' in dict_obj:
        obj.max_phase_for_all_diseases = evidence_drug.Diseasephase.fromDict(dict_obj['max_phase_for_all_diseases'])
    if  'withdrawn_country' in dict_obj:
        obj.withdrawn_country = dict_obj['withdrawn_country']
    if  'withdrawn_reason' in dict_obj:
        obj.withdrawn_reason = dict_obj['withdrawn_reason']
    if  'withdrawn_year' in dict_obj:
        obj.withdrawn_year = dict_obj['withdrawn_year']
    for key in dict_obj:
      if not key in cls_keys:
        logger.warn("Drug - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Drug
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Drug, self).validate(logger, path = path)
    if self.id is None:
      logger.error("Drug - {0}.id is required".format(path))
      error = error + 1
    # id is mandatory
    if self.id is None :
        logger.error("Drug - {0}.id is required".format(path))
        error = error + 1
    """ Check regex: ^http://identifiers.org/chembl.compound/CHEMBL[0-9]+$|^http://private/.+$ for validation"""
    if self.id is not None and not re.match('^http://identifiers.org/chembl.compound/CHEMBL[0-9]+$|^http://private/.+$', self.id):
        logger.error("Drug - {0}.id '{1}'".format(path,self.id) + " does not match pattern '^http://identifiers.org/chembl.compound/CHEMBL[0-9]+$|^http://private/.+$'")
        logger.warn(json.dumps(self.id, sort_keys=True, indent=2))
    if self.id is not None and not isinstance(self.id, six.string_types):
        logger.error("Drug - {0}.id type should be a string".format(path))
        error = error + 1
    # molecule_name is mandatory
    if self.molecule_name is None :
        logger.error("Drug - {0}.molecule_name is required".format(path))
        error = error + 1
    if self.molecule_name is not None and not isinstance(self.molecule_name, six.string_types):
        logger.error("Drug - {0}.molecule_name type should be a string".format(path))
        error = error + 1
    # molecule_type is mandatory
    if self.molecule_type is None :
        logger.error("Drug - {0}.molecule_type is required".format(path))
        error = error + 1
    if self.molecule_type is not None and not isinstance(self.molecule_type, six.string_types):
        logger.error("Drug - {0}.molecule_type type should be a string".format(path))
        error = error + 1
    if self.max_phase_for_all_diseases:
        if not isinstance(self.max_phase_for_all_diseases, evidence_drug.Diseasephase):
            logger.error("evidence_drug.Diseasephase class instance expected for attribute - {0}.max_phase_for_all_diseases".format(path))
            error = error + 1
        else:
            max_phase_for_all_diseases_error = self.max_phase_for_all_diseases.validate(logger, path = '.'.join([path, 'max_phase_for_all_diseases']))
            error = error + max_phase_for_all_diseases_error
    if self.withdrawn_country is not None and not isinstance(self.withdrawn_country, six.string_types):
        logger.error("Drug - {0}.withdrawn_country type should be a string".format(path))
        error = error + 1
    if self.withdrawn_reason is not None and not isinstance(self.withdrawn_reason, six.string_types):
        logger.error("Drug - {0}.withdrawn_reason type should be a string".format(path))
        error = error + 1
    if self.withdrawn_year is not None and not isinstance(self.withdrawn_year, six.string_types):
        logger.error("Drug - {0}.withdrawn_year type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = super(Drug, self).serialize()
    if not self.id is None: classDict['id'] = self.id
    if not self.molecule_name is None: classDict['molecule_name'] = self.molecule_name
    if not self.molecule_type is None: classDict['molecule_type'] = self.molecule_type
    if not self.max_phase_for_all_diseases is None: classDict['max_phase_for_all_diseases'] = self.max_phase_for_all_diseases.serialize()
    if not self.withdrawn_country is None: classDict['withdrawn_country'] = self.withdrawn_country
    if not self.withdrawn_reason is None: classDict['withdrawn_reason'] = self.withdrawn_reason
    if not self.withdrawn_year is None: classDict['withdrawn_year'] = self.withdrawn_year
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/bioentity/variant.json
"""
class Variant(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param id = None
  """
  def __init__(self, type = None, id = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Variant, self).__init__(id = id)
    
    """
    Name: id
    Type: string
    Description: An array of variant identifiers
    Can be null: False
    Required: {True}
    """
    self.id = id
    
    """
    Name: type
    Type: string
    Can be null: False
    Required: {True}
    """
    self.type = type
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Variant, cls).cloneObject(clone)
    if clone.id:
        obj.id = clone.id
    if clone.type:
        obj.type = clone.type
    return obj
  
  @classmethod
  def fromDict(cls, dict_obj):
    cls_keys = ['id','type','id']
    obj = super(Variant, cls).fromDict(dict_obj)
    if not isinstance(dict_obj, dict):
      logger.warn("Variant - DictType expected - {0} found\n".format(type(dict_obj)))
      return
    if  'id' in dict_obj:
        obj.id = dict_obj['id']
    if  'type' in dict_obj:
        obj.type = dict_obj['type']
    for key in dict_obj:
      if not key in cls_keys:
        logger.warn("Variant - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Variant
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Variant, self).validate(logger, path = path)
    if self.id is None:
      logger.error("Variant - {0}.id is required".format(path))
      error = error + 1
    # id is mandatory
    if self.id is None :
        logger.error("Variant - {0}.id is required".format(path))
        error = error + 1
    """ Check regex: ^http://www.ncbi.nlm.nih.gov/clinvar/RCV[0-9]{9}|http://identifiers.org/dbsnp/rs[0-9]{1,}|http://identifiers.org/dbsnp/esv[0-9]{1,}|http://identifiers.org/dbsnp/nsv[0-9]{1,}$ for validation"""
    if self.id is not None and not re.match('^http://www.ncbi.nlm.nih.gov/clinvar/RCV[0-9]{9}|http://identifiers.org/dbsnp/rs[0-9]{1,}|http://identifiers.org/dbsnp/esv[0-9]{1,}|http://identifiers.org/dbsnp/nsv[0-9]{1,}$', self.id):
        logger.error("Variant - {0}.id '{1}'".format(path,self.id) + " does not match pattern '^http://www.ncbi.nlm.nih.gov/clinvar/RCV[0-9]{9}|http://identifiers.org/dbsnp/rs[0-9]{1,}|http://identifiers.org/dbsnp/esv[0-9]{1,}|http://identifiers.org/dbsnp/nsv[0-9]{1,}$'")
        logger.warn(json.dumps(self.id, sort_keys=True, indent=2))
    if self.id is not None and not isinstance(self.id, six.string_types):
        logger.error("Variant - {0}.id type should be a string".format(path))
        error = error + 1
    # type is mandatory
    if self.type is None :
        logger.error("Variant - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['snp single','snp snp interaction','structural variant']:
        logger.error("Variant - {0}.type value is restricted to the fixed set of values 'snp single','snp snp interaction','structural variant' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type is not None and not isinstance(self.type, six.string_types):
        logger.error("Variant - {0}.type type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = super(Variant, self).serialize()
    if not self.id is None: classDict['id'] = self.id
    if not self.type is None: classDict['type'] = self.type
    return classDict
  
  def to_JSON(self, indentation=4):
    if sys.version_info[0] == 3:
      return json.dumps(self.serialize(), sort_keys=True, check_circular=False, indent=indentation)
    elif sys.version_info[0] == 2:
      return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
