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
import opentargets.model.evidence.drug as evidence_drug

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
    """
    self.id = id
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.id:
        obj.id = clone.id
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['id']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("Base - DictType expected - {0} found\n".format(type(map)))
      return
    if  'id' in map:
        obj.id = map['id']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Base
    :returns: number of errors found during validation
    """
    error = 0
    if self.id and not isinstance(self.id, six.string_types):
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
    Required: {True}
    """
    self.id = id
    
    """
    Name: name
    Type: string
    Description: Optional - EFO disease name corresponding to the EFO ID
    """
    self.name = name
    
    """
    Name: source_name
    Type: string
    Description: Optional - EFO disease name corresponding to the EFO ID
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
  def fromMap(cls, map):
    cls_keys = ['id','name','source_name','biosample','id']
    obj = super(Disease, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Disease - DictType expected - {0} found\n".format(type(map)))
      return
    if  'id' in map:
        obj.id = map['id']
    if  'name' in map:
        obj.name = map['name']
    if  'source_name' in map:
        obj.source_name = map['source_name']
    if  'biosample' in map:
        obj.biosample = DiseaseBiosample.fromMap(map['biosample'])
    for key in map:
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
    if self.id and not re.match('^http://purl.bioontology.org/omim/OMIM_[0-9]{1,}|http://www.orpha.net/ORDO/Orphanet_[0-9]{1,}|http://purl.obolibrary.org/obo/DOID_[0-9]{2,}|http://www.ebi.ac.uk/efo/EFO_[0-9]{7,}|http://purl.obolibrary.org/obo/HP_[0-9]{4,}|http://purl.obolibrary.org/obo/GO_[0-9]{4,}|http://purl.obolibrary.org/obo/MP_[0-9]{3,}|http://purl.obolibrary.org/obo/MPATH_[0-9]{3,}$', self.id):
        logger.error("Disease - {0}.id '{1}'".format(path,self.id) + " does not match pattern '^http://purl.bioontology.org/omim/OMIM_[0-9]{1,}|http://www.orpha.net/ORDO/Orphanet_[0-9]{1,}|http://purl.obolibrary.org/obo/DOID_[0-9]{2,}|http://www.ebi.ac.uk/efo/EFO_[0-9]{7,}|http://purl.obolibrary.org/obo/HP_[0-9]{4,}|http://purl.obolibrary.org/obo/GO_[0-9]{4,}|http://purl.obolibrary.org/obo/MP_[0-9]{3,}|http://purl.obolibrary.org/obo/MPATH_[0-9]{3,}$'")
        logger.warn(json.dumps(self.id, sort_keys=True, indent=2))
    if self.id and not isinstance(self.id, six.string_types):
        logger.error("Disease - {0}.id type should be a string".format(path))
        error = error + 1
    if self.name and not isinstance(self.name, six.string_types):
        logger.error("Disease - {0}.name type should be a string".format(path))
        error = error + 1
    if self.source_name and not isinstance(self.source_name, six.string_types):
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
    Required: {True}
    """
    self.name = name
    
    """
    Name: id
    Type: string
    Description: EFO ID of the tissue - optional
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
  def fromMap(cls, map):
    cls_keys = ['name','id']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("DiseaseBiosample - DictType expected - {0} found\n".format(type(map)))
      return
    if  'name' in map:
        obj.name = map['name']
    if  'id' in map:
        obj.id = map['id']
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
    if self.name and not isinstance(self.name, six.string_types):
        logger.error("DiseaseBiosample - {0}.name type should be a string".format(path))
        error = error + 1
    if self.id and not isinstance(self.id, six.string_types):
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
    Required: {True}
    """
    self.id = id
    
    """
    Name: tier
    Type: string
    Description: Cancer Gene Census genes has been split into two tiers
    """
    self.tier = tier
    
    """
    Name: complex_id
    Type: string
    Description: A ChEMBL protein complex identifier
    """
    self.complex_id = complex_id
    
    """
    Name: complex_members
    Type: array
    """
    self.complex_members = complex_members
    
    """
    Name: complex_type
    Type: string
    Description: Type of target
    """
    self.complex_type = complex_type
    
    """
    Name: target_type
    Type: string
    Description: Type of target; if you do not have detailed information, select from gene_evidence, protein_evidence or transcript_evidence
    Required: {True}
    """
    self.target_type = target_type
    
    """
    Name: activity
    Type: string
    Description: Activity of target in disease context
    Required: {True}
    """
    self.activity = activity
    
    """
    Name: target_name
    Type: string
    Description: used by ChEMBL initially if they have a more canonical target name, optional
    """
    self.target_name = target_name
    
    """
    Name: target_class
    Type: array
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
  def fromMap(cls, map):
    cls_keys = ['id','tier','complex_id','complex_members','complex_type','target_type','activity','target_name','target_class','id']
    obj = super(Target, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Target - DictType expected - {0} found\n".format(type(map)))
      return
    if  'id' in map:
        obj.id = map['id']
    if  'tier' in map:
        obj.tier = map['tier']
    if  'complex_id' in map:
        obj.complex_id = map['complex_id']
    if  'complex_members' in map:
        obj.complex_members = map['complex_members']
    if  'complex_type' in map:
        obj.complex_type = map['complex_type']
    if  'target_type' in map:
        obj.target_type = map['target_type']
    if  'activity' in map:
        obj.activity = map['activity']
    if  'target_name' in map:
        obj.target_name = map['target_name']
    if  'target_class' in map:
        obj.target_class = map['target_class']
    for key in map:
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
    if self.id and not re.match('^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$', self.id):
        logger.error("Target - {0}.id '{1}'".format(path,self.id) + " does not match pattern '^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$'")
        logger.warn(json.dumps(self.id, sort_keys=True, indent=2))
    if self.id and not isinstance(self.id, six.string_types):
        logger.error("Target - {0}.id type should be a string".format(path))
        error = error + 1
    if not self.tier is None and not self.tier in ['tier 1','tier 2']:
        logger.error("Target - {0}.tier value is restricted to the fixed set of values 'tier 1','tier 2' ('{1}' given)".format(path, self.tier))
        error = error + 1
    if self.tier and not isinstance(self.tier, six.string_types):
        logger.error("Target - {0}.tier type should be a string".format(path))
        error = error + 1
    """ Check regex: ^CHEMBL[0-9]+$ for validation"""
    if self.complex_id and not re.match('^CHEMBL[0-9]+$', self.complex_id):
        logger.error("Target - {0}.complex_id '{1}'".format(path,self.complex_id) + " does not match pattern '^CHEMBL[0-9]+$'")
        logger.warn(json.dumps(self.complex_id, sort_keys=True, indent=2))
    if self.complex_id and not isinstance(self.complex_id, six.string_types):
        logger.error("Target - {0}.complex_id type should be a string".format(path))
        error = error + 1
    if not self.complex_members is None and len(self.complex_members) > 0 and not all(isinstance(n, six.string_types) for n in self.complex_members):
        logger.error("Target - {0}.complex_members array should have elements of type 'six.string_types'".format(path))
        error = error+1
    if self.complex_members and len(self.complex_members) < 1:
        logger.error("Target - {0}.complex_members array should have at least 1 elements".format(path))
        error = error + 1
    if self.complex_members and len(set(self.complex_members)) != len(self.complex_members):
        logger.error("Target - {0}.complex_members array have duplicated elements".format(path))
        error = error + 1
    """ Check regex: ^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$ for validation of array item"""
    if self.complex_members and len(self.complex_members) > 0 and not all(re.match('^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$', n) for n in self.complex_members):
        logger.error("Target - {0}.complex_members items".format(path) + " do not match pattern '^http://identifiers.org/ensembl/ENSG[0-9]{4,}$|^http://identifiers.org/uniprot/.{4,}$'")
    if not self.complex_type is None and not self.complex_type in ['http://identifiers.org/cttv.target/chimeric_protein','http://identifiers.org/cttv.target/protein_complex','http://identifiers.org/cttv.target/protein_complex_group','http://identifiers.org/cttv.target/protein_complex_heteropolymer','http://identifiers.org/cttv.target/protein_complex_homopolymer','http://identifiers.org/cttv.target/protein_family','http://identifiers.org/cttv.target/selectivity_group']:
        logger.error("Target - {0}.complex_type value is restricted to the fixed set of values 'http://identifiers.org/cttv.target/chimeric_protein','http://identifiers.org/cttv.target/protein_complex','http://identifiers.org/cttv.target/protein_complex_group','http://identifiers.org/cttv.target/protein_complex_heteropolymer','http://identifiers.org/cttv.target/protein_complex_homopolymer','http://identifiers.org/cttv.target/protein_family','http://identifiers.org/cttv.target/selectivity_group' ('{1}' given)".format(path, self.complex_type))
        error = error + 1
    if self.complex_type and not isinstance(self.complex_type, six.string_types):
        logger.error("Target - {0}.complex_type type should be a string".format(path))
        error = error + 1
    # target_type is mandatory
    if self.target_type is None :
        logger.error("Target - {0}.target_type is required".format(path))
        error = error + 1
    if not self.target_type is None and not self.target_type in ['http://identifiers.org/cttv.target/gene_allele','http://identifiers.org/cttv.target/gene_evidence','http://identifiers.org/cttv.target/gene_in_LD_region','http://identifiers.org/cttv.target/gene_in_epigenetic_regulation_complex','http://identifiers.org/cttv.target/gene_variant','http://identifiers.org/cttv.target/pro_protein','http://identifiers.org/cttv.target/protein_evidence','http://identifiers.org/cttv.target/transcript_evidence','http://identifiers.org/cttv.target/transcript_isoform','http://identifiers.org/cttv.target/protein_isoform','http://identifiers.org/cttv.target/gene_or_protein_or_transcript']:
        logger.error("Target - {0}.target_type value is restricted to the fixed set of values 'http://identifiers.org/cttv.target/gene_allele','http://identifiers.org/cttv.target/gene_evidence','http://identifiers.org/cttv.target/gene_in_LD_region','http://identifiers.org/cttv.target/gene_in_epigenetic_regulation_complex','http://identifiers.org/cttv.target/gene_variant','http://identifiers.org/cttv.target/pro_protein','http://identifiers.org/cttv.target/protein_evidence','http://identifiers.org/cttv.target/transcript_evidence','http://identifiers.org/cttv.target/transcript_isoform','http://identifiers.org/cttv.target/protein_isoform','http://identifiers.org/cttv.target/gene_or_protein_or_transcript' ('{1}' given)".format(path, self.target_type))
        error = error + 1
    if self.target_type and not isinstance(self.target_type, six.string_types):
        logger.error("Target - {0}.target_type type should be a string".format(path))
        error = error + 1
    # activity is mandatory
    if self.activity is None :
        logger.error("Target - {0}.activity is required".format(path))
        error = error + 1
    if not self.activity is None and not self.activity in ['http://identifiers.org/cttv.activity/decreased_transcript_level','http://identifiers.org/cttv.activity/decreased_translational_product_level','http://identifiers.org/cttv.activity/drug_negative_modulator','http://identifiers.org/cttv.activity/drug_positive_modulator','http://identifiers.org/cttv.activity/gain_of_function','http://identifiers.org/cttv.activity/increased_transcript_level','http://identifiers.org/cttv.activity/increased_translational_product_level','http://identifiers.org/cttv.activity/loss_of_function','http://identifiers.org/cttv.activity/partial_loss_of_function','http://identifiers.org/cttv.activity/up_or_down','http://identifiers.org/cttv.activity/up','http://identifiers.org/cttv.activity/down','http://identifiers.org/cttv.activity/tolerated','http://identifiers.org/cttv.activity/predicted','http://identifiers.org/cttv.activity/damaging','http://identifiers.org/cttv.activity/damaging_to_target','http://identifiers.org/cttv.activity/predicted_tolerated','http://identifiers.org/cttv.activity/predicted_damaging','http://identifiers.org/cttv.activity/tolerated_by_target','http://identifiers.org/cttv.activity/unknown']:
        logger.error("Target - {0}.activity value is restricted to the fixed set of values 'http://identifiers.org/cttv.activity/decreased_transcript_level','http://identifiers.org/cttv.activity/decreased_translational_product_level','http://identifiers.org/cttv.activity/drug_negative_modulator','http://identifiers.org/cttv.activity/drug_positive_modulator','http://identifiers.org/cttv.activity/gain_of_function','http://identifiers.org/cttv.activity/increased_transcript_level','http://identifiers.org/cttv.activity/increased_translational_product_level','http://identifiers.org/cttv.activity/loss_of_function','http://identifiers.org/cttv.activity/partial_loss_of_function','http://identifiers.org/cttv.activity/up_or_down','http://identifiers.org/cttv.activity/up','http://identifiers.org/cttv.activity/down','http://identifiers.org/cttv.activity/tolerated','http://identifiers.org/cttv.activity/predicted','http://identifiers.org/cttv.activity/damaging','http://identifiers.org/cttv.activity/damaging_to_target','http://identifiers.org/cttv.activity/predicted_tolerated','http://identifiers.org/cttv.activity/predicted_damaging','http://identifiers.org/cttv.activity/tolerated_by_target','http://identifiers.org/cttv.activity/unknown' ('{1}' given)".format(path, self.activity))
        error = error + 1
    if self.activity and not isinstance(self.activity, six.string_types):
        logger.error("Target - {0}.activity type should be a string".format(path))
        error = error + 1
    if self.target_name and not isinstance(self.target_name, six.string_types):
        logger.error("Target - {0}.target_name type should be a string".format(path))
        error = error + 1
    if not self.target_class is None and len(self.target_class) > 0 and not all(isinstance(n, six.string_types) for n in self.target_class):
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
    Required: {True}
    """
    self.term_id = term_id
    
    """
    Name: label
    Type: string
    Description: Phenotype term label
    Required: {True}
    """
    self.label = label
    
    """
    Name: species
    Type: string
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
  def fromMap(cls, map):
    cls_keys = ['term_id','label','species','id']
    obj = super(Phenotype, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Phenotype - DictType expected - {0} found\n".format(type(map)))
      return
    if  'term_id' in map:
        obj.term_id = map['term_id']
    if  'label' in map:
        obj.label = map['label']
    if  'species' in map:
        obj.species = map['species']
    for key in map:
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
    if self.term_id and not re.match('^http://purl.obolibrary.org/obo/HP_[0-9]{4,}||http://purl.obolibrary.org/obo/MP_[0-9]{4,}$', self.term_id):
        logger.error("Phenotype - {0}.term_id '{1}'".format(path,self.term_id) + " does not match pattern '^http://purl.obolibrary.org/obo/HP_[0-9]{4,}||http://purl.obolibrary.org/obo/MP_[0-9]{4,}$'")
        logger.warn(json.dumps(self.term_id, sort_keys=True, indent=2))
    if self.term_id and not isinstance(self.term_id, six.string_types):
        logger.error("Phenotype - {0}.term_id type should be a string".format(path))
        error = error + 1
    # label is mandatory
    if self.label is None :
        logger.error("Phenotype - {0}.label is required".format(path))
        error = error + 1
    if self.label and not isinstance(self.label, six.string_types):
        logger.error("Phenotype - {0}.label type should be a string".format(path))
        error = error + 1
    # species is mandatory
    if self.species is None :
        logger.error("Phenotype - {0}.species is required".format(path))
        error = error + 1
    if not self.species is None and not self.species in ['mouse','human','rat','zebrafish','dog']:
        logger.error("Phenotype - {0}.species value is restricted to the fixed set of values 'mouse','human','rat','zebrafish','dog' ('{1}' given)".format(path, self.species))
        error = error + 1
    if self.species and not isinstance(self.species, six.string_types):
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
  :param id = None
  """
  def __init__(self, molecule_name = None, molecule_type = None,     max_phase_for_all_diseases = None, id = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Drug, self).__init__(id = id)
    
    """
    Name: id
    Type: string
    Description: A ChEMBL or internal drug identifier
    Required: {True}
    """
    self.id = id
    
    """
    Name: molecule_name
    Type: string
    Required: {True}
    """
    self.molecule_name = molecule_name
    
    """
    Name: molecule_type
    Type: string
    Required: {True}
    """
    self.molecule_type = molecule_type
    """
    Name: max_phase_for_all_diseases
    """
    self.max_phase_for_all_diseases = max_phase_for_all_diseases
  
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
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['id','molecule_name','molecule_type','max_phase_for_all_diseases','id']
    obj = super(Drug, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Drug - DictType expected - {0} found\n".format(type(map)))
      return
    if  'id' in map:
        obj.id = map['id']
    if  'molecule_name' in map:
        obj.molecule_name = map['molecule_name']
    if  'molecule_type' in map:
        obj.molecule_type = map['molecule_type']
    if  'max_phase_for_all_diseases' in map:
        obj.max_phase_for_all_diseases = evidence_drug.Diseasephase.fromMap(map['max_phase_for_all_diseases'])
    for key in map:
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
    if self.id and not re.match('^http://identifiers.org/chembl.compound/CHEMBL[0-9]+$|^http://private/.+$', self.id):
        logger.error("Drug - {0}.id '{1}'".format(path,self.id) + " does not match pattern '^http://identifiers.org/chembl.compound/CHEMBL[0-9]+$|^http://private/.+$'")
        logger.warn(json.dumps(self.id, sort_keys=True, indent=2))
    if self.id and not isinstance(self.id, six.string_types):
        logger.error("Drug - {0}.id type should be a string".format(path))
        error = error + 1
    # molecule_name is mandatory
    if self.molecule_name is None :
        logger.error("Drug - {0}.molecule_name is required".format(path))
        error = error + 1
    if self.molecule_name and not isinstance(self.molecule_name, six.string_types):
        logger.error("Drug - {0}.molecule_name type should be a string".format(path))
        error = error + 1
    # molecule_type is mandatory
    if self.molecule_type is None :
        logger.error("Drug - {0}.molecule_type is required".format(path))
        error = error + 1
    if self.molecule_type and not isinstance(self.molecule_type, six.string_types):
        logger.error("Drug - {0}.molecule_type type should be a string".format(path))
        error = error + 1
    if self.max_phase_for_all_diseases:
        if not isinstance(self.max_phase_for_all_diseases, evidence_drug.Diseasephase):
            logger.error("evidence_drug.Diseasephase class instance expected for attribute - {0}.max_phase_for_all_diseases".format(path))
            error = error + 1
        else:
            max_phase_for_all_diseases_error = self.max_phase_for_all_diseases.validate(logger, path = '.'.join([path, 'max_phase_for_all_diseases']))
            error = error + max_phase_for_all_diseases_error
    return error
  
  def serialize(self):
    classDict = super(Drug, self).serialize()
    if not self.id is None: classDict['id'] = self.id
    if not self.molecule_name is None: classDict['molecule_name'] = self.molecule_name
    if not self.molecule_type is None: classDict['molecule_type'] = self.molecule_type
    if not self.max_phase_for_all_diseases is None: classDict['max_phase_for_all_diseases'] = self.max_phase_for_all_diseases.serialize()
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
    Required: {True}
    """
    self.id = id
    
    """
    Name: type
    Type: string
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
  def fromMap(cls, map):
    cls_keys = ['id','type','id']
    obj = super(Variant, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Variant - DictType expected - {0} found\n".format(type(map)))
      return
    if  'id' in map:
        obj.id = map['id']
    if  'type' in map:
        obj.type = map['type']
    for key in map:
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
    if self.id and not re.match('^http://www.ncbi.nlm.nih.gov/clinvar/RCV[0-9]{9}|http://identifiers.org/dbsnp/rs[0-9]{1,}|http://identifiers.org/dbsnp/esv[0-9]{1,}|http://identifiers.org/dbsnp/nsv[0-9]{1,}$', self.id):
        logger.error("Variant - {0}.id '{1}'".format(path,self.id) + " does not match pattern '^http://www.ncbi.nlm.nih.gov/clinvar/RCV[0-9]{9}|http://identifiers.org/dbsnp/rs[0-9]{1,}|http://identifiers.org/dbsnp/esv[0-9]{1,}|http://identifiers.org/dbsnp/nsv[0-9]{1,}$'")
        logger.warn(json.dumps(self.id, sort_keys=True, indent=2))
    if self.id and not isinstance(self.id, six.string_types):
        logger.error("Variant - {0}.id type should be a string".format(path))
        error = error + 1
    # type is mandatory
    if self.type is None :
        logger.error("Variant - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['snp single','snp snp interaction','structural variant']:
        logger.error("Variant - {0}.type value is restricted to the fixed set of values 'snp single','snp snp interaction','structural variant' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type and not isinstance(self.type, six.string_types):
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
