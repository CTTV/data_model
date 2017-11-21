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
import opentargets.model.bioentity as bioentity
import opentargets.model.evidence.core as evidence_core
import opentargets.model.evidence.phenotype as evidence_phenotype
import opentargets.model.evidence.drug as evidence_drug
import opentargets.model.evidence.genetics as evidence_genetics

__author__ = "Gautier Koscielny"
__copyright__ = "Copyright 2014-2017, Open Targets"
__credits__ = ["Gautier Koscielny", "Samiul Hasan"]
__license__ = "Apache 2.0"
__version__ = "1.2.7"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautierk@targetvalidation.org"
__status__ = "Production"

logger = logging.getLogger(__name__)

class JSONException(Exception):
  pass


"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/base.json
"""
class Base(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param sourceID = None
  :param access_level = None
  :param validated_against_schema_version = None
  :param unique_association_fields = None
  :param     target = None
  :param     disease = None
  :param     literature = None
  """
  def __init__(self, sourceID = None, access_level = None, validated_against_schema_version = None, unique_association_fields = None,     target = None,     disease = None,     literature = None):
    
    """
    Name: sourceID
    Type: string
    Description: A source ID (database or study ID) to help identify who this data is from.
    """
    self.sourceID = sourceID
    
    """
    Name: access_level
    Type: string
    Description: Choose public as default; private is for internal datasets
    """
    self.access_level = access_level
    
    """
    Name: validated_against_schema_version
    Type: string
    Description: The OpenTargets-JSON schema version number against which your data was validated
    """
    self.validated_against_schema_version = validated_against_schema_version
    """
    Name: unique_association_fields
    """
    self.unique_association_fields = unique_association_fields
    """
    Name: target
    """
    self.target = target
    """
    Name: disease
    """
    self.disease = disease
    """
    Name: literature
    """
    self.literature = literature
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.sourceID:
        obj.sourceID = clone.sourceID
    if clone.access_level:
        obj.access_level = clone.access_level
    if clone.validated_against_schema_version:
        obj.validated_against_schema_version = clone.validated_against_schema_version
    if clone.unique_association_fields:
        obj.unique_association_fields = clone.unique_association_fields
    if clone.target:
        obj.target = bioentity.Target.cloneObject(clone.target)
    if clone.disease:
        obj.disease = bioentity.Disease.cloneObject(clone.disease)
    if clone.literature:
        obj.literature = BaseLiterature.cloneObject(clone.literature)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['sourceID','access_level','validated_against_schema_version','unique_association_fields','target','disease','literature']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("Base - DictType expected - {0} found\n".format(type(map)))
      return
    if  'sourceID' in map:
        obj.sourceID = map['sourceID']
    if  'access_level' in map:
        obj.access_level = map['access_level']
    if  'validated_against_schema_version' in map:
        obj.validated_against_schema_version = map['validated_against_schema_version']
    if  'unique_association_fields' in map:
        obj.unique_association_fields = map['unique_association_fields']
    if  'target' in map:
        obj.target = bioentity.Target.fromMap(map['target'])
    if  'disease' in map:
        obj.disease = bioentity.Disease.fromMap(map['disease'])
    if  'literature' in map:
        obj.literature = BaseLiterature.fromMap(map['literature'])
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Base
    :returns: number of errors found during validation
    """
    error = 0
    """ Check regex: ^[a-z0-9_]+$ for validation"""
    if self.sourceID and not re.match('^[a-z0-9_]+$', self.sourceID):
        logger.error("Base - {0}.sourceID '{1}'".format(path,self.sourceID) + " does not match pattern '^[a-z0-9_]+$'")
        logger.warn(json.dumps(self.sourceID, sort_keys=True, indent=2))
    if self.sourceID and not isinstance(self.sourceID, basestring):
        logger.error("Base - {0}.sourceID type should be a string".format(path))
        error = error + 1
    if not self.access_level is None and not self.access_level in ['public','private']:
        logger.error("Base - {0}.access_level value is restricted to the fixed set of values 'public','private' ('{1}' given)".format(path, self.access_level))
        error = error + 1
    if self.access_level and not isinstance(self.access_level, basestring):
        logger.error("Base - {0}.access_level type should be a string".format(path))
        error = error + 1
    if not self.validated_against_schema_version is None and not self.validated_against_schema_version in ['1.2.7']:
        logger.error("Base - {0}.validated_against_schema_version value is restricted to the fixed set of values '1.2.7' ('{1}' given)".format(path, self.validated_against_schema_version))
        error = error + 1
    if self.validated_against_schema_version and not isinstance(self.validated_against_schema_version, basestring):
        logger.error("Base - {0}.validated_against_schema_version type should be a string".format(path))
        error = error + 1
    if self.unique_association_fields and not isinstance(self.unique_association_fields, dict):
        logger.error("Basedictionary expected for attribute - {0}.unique_association_fields".format(path))
        error = error + 1
    if self.target:
        if not isinstance(self.target, bioentity.Target):
            logger.error("bioentity.Target class instance expected for attribute - {0}.target".format(path))
            error = error + 1
        else:
            target_error = self.target.validate(logger, path = '.'.join([path, 'target']))
            error = error + target_error
    if self.disease:
        if not isinstance(self.disease, bioentity.Disease):
            logger.error("bioentity.Disease class instance expected for attribute - {0}.disease".format(path))
            error = error + 1
        else:
            disease_error = self.disease.validate(logger, path = '.'.join([path, 'disease']))
            error = error + disease_error
    if self.literature:
        if not isinstance(self.literature, BaseLiterature):
            logger.error("BaseLiterature class instance expected for attribute - {0}.literature".format(path))
            error = error + 1
        else:
            literature_error = self.literature.validate(logger, path = '.'.join([path, 'literature']))
            error = error + literature_error
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.sourceID is None: classDict['sourceID'] = self.sourceID
    if not self.access_level is None: classDict['access_level'] = self.access_level
    if not self.validated_against_schema_version is None: classDict['validated_against_schema_version'] = self.validated_against_schema_version
    if not self.unique_association_fields is None: classDict['unique_association_fields'] = self.unique_association_fields
    if not self.target is None: classDict['target'] = self.target.serialize()
    if not self.disease is None: classDict['disease'] = self.disease.serialize()
    if not self.literature is None: classDict['literature'] = self.literature.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/base.json inner class:(literature)
"""
class BaseLiterature(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param references = None
  """
  def __init__(self, references = None):
    
    """
    Name: references
    Type: array
    """
    self.references = references
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.references:
        obj.references = []; obj.references.extend(clone.references)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['references']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("BaseLiterature - DictType expected - {0} found\n".format(type(map)))
      return
    if 'references' in map and isinstance(map['references'], list):
        obj.references = []
        for item in map['references']:
            obj.references.append(evidence_core.Single_Lit_Reference.fromMap(item))
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class BaseLiterature
    :returns: number of errors found during validation
    """
    error = 0
    if not self.references is None and len(self.references) > 0 and not all(isinstance(n, evidence_core.Single_Lit_Reference) for n in self.references):
        logger.error("BaseLiterature - {0}.references array should have elements of type 'evidence_core.Single_Lit_Reference'".format(path))
        error = error+1
    if self.references and len(self.references) < 1:
        logger.error("BaseLiterature - {0}.references array should have at least 1 elements".format(path))
        error = error + 1
    if self.references and len(set(self.references)) != len(self.references):
        logger.error("BaseLiterature - {0}.references array have duplicated elements".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.references is None: classDict['references'] = map(lambda x: x.serialize(), self.references)
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/animal_models.json
"""
class Animal_Models(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param evidence = None
  :param sourceID = None
  :param access_level = None
  :param validated_against_schema_version = None
  :param unique_association_fields = None
  :param     target = None
  :param     disease = None
  :param     literature = None
  """
  def __init__(self, type = None, evidence = None, sourceID = None, access_level = None, validated_against_schema_version = None, unique_association_fields = None,     target = None,     disease = None,     literature = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Animal_Models, self).__init__(sourceID = sourceID,access_level = access_level,validated_against_schema_version = validated_against_schema_version,unique_association_fields = unique_association_fields,target = target,disease = disease,literature = literature)
    
    """
    Name: type
    Type: string
    Required: {True}
    """
    self.type = type
    """
    Name: evidence
    """
    self.evidence = evidence
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Animal_Models, cls).cloneObject(clone)
    if clone.type:
        obj.type = clone.type
    obj.evidence = Animal_ModelsEvidence.cloneObject(clone.evidence)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['type','evidence','sourceID','access_level','validated_against_schema_version','unique_association_fields','target','disease','literature']
    obj = super(Animal_Models, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Animal_Models - DictType expected - {0} found\n".format(type(map)))
      return
    if  'type' in map:
        obj.type = map['type']
    if  'evidence' in map:
        obj.evidence = Animal_ModelsEvidence.fromMap(map['evidence'])
    for key in map:
      if not key in cls_keys:
        logger.warn("Animal_Models - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Animal_Models
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Animal_Models, self).validate(logger, path = path)
    if self.sourceID is None:
      logger.error("Animal_Models - {0}.sourceID is required".format(path))
      error = error + 1
    if self.access_level is None:
      logger.error("Animal_Models - {0}.access_level is required".format(path))
      error = error + 1
    if self.validated_against_schema_version is None:
      logger.error("Animal_Models - {0}.validated_against_schema_version is required".format(path))
      error = error + 1
    if self.unique_association_fields is None:
      logger.error("Animal_Models - {0}.unique_association_fields is required".format(path))
      error = error + 1
    if self.target is None:
      logger.error("Animal_Models - {0}.target is required".format(path))
      error = error + 1
    if self.disease is None:
      logger.error("Animal_Models - {0}.disease is required".format(path))
      error = error + 1
    # type is mandatory
    if self.type is None :
        logger.error("Animal_Models - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['animal_model']:
        logger.error("Animal_Models - {0}.type value is restricted to the fixed set of values 'animal_model' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type and not isinstance(self.type, basestring):
        logger.error("Animal_Models - {0}.type type should be a string".format(path))
        error = error + 1
    if self.evidence is None:
        logger.error("Animal_Models - {0}.evidence is required".format(path))
        error = error + 1
    elif not isinstance(self.evidence, Animal_ModelsEvidence):
        logger.error("Animal_ModelsEvidence class instance expected for attribute - {0}.evidence".format(path))
        error = error + 1
    else:
        evidence_error = self.evidence.validate(logger, path = '.'.join([path, 'evidence']))
        error = error + evidence_error
    return error
  
  def serialize(self):
    classDict = super(Animal_Models, self).serialize()
    if not self.type is None: classDict['type'] = self.type
    if not self.evidence is None: classDict['evidence'] = self.evidence.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/animal_models.json inner class:(evidence)
"""
class Animal_ModelsEvidence(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param orthologs = None
  :param biological_model = None
  :param disease_model_association = None
  """
  def __init__(self, orthologs = None, biological_model = None, disease_model_association = None):
    """
    Name: orthologs
    """
    self.orthologs = orthologs
    """
    Name: biological_model
    """
    self.biological_model = biological_model
    """
    Name: disease_model_association
    """
    self.disease_model_association = disease_model_association
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    obj.orthologs = evidence_phenotype.Orthologs.cloneObject(clone.orthologs)
    obj.biological_model = evidence_phenotype.Biological_Model.cloneObject(clone.biological_model)
    obj.disease_model_association = evidence_phenotype.Disease_Model_Association.cloneObject(clone.disease_model_association)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['orthologs','biological_model','disease_model_association']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("Animal_ModelsEvidence - DictType expected - {0} found\n".format(type(map)))
      return
    if  'orthologs' in map:
        obj.orthologs = evidence_phenotype.Orthologs.fromMap(map['orthologs'])
    if  'biological_model' in map:
        obj.biological_model = evidence_phenotype.Biological_Model.fromMap(map['biological_model'])
    if  'disease_model_association' in map:
        obj.disease_model_association = evidence_phenotype.Disease_Model_Association.fromMap(map['disease_model_association'])
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Animal_ModelsEvidence
    :returns: number of errors found during validation
    """
    error = 0
    if self.orthologs is None:
        logger.error("Animal_ModelsEvidence - {0}.orthologs is required".format(path))
        error = error + 1
    elif not isinstance(self.orthologs, evidence_phenotype.Orthologs):
        logger.error("evidence_phenotype.Orthologs class instance expected for attribute - {0}.orthologs".format(path))
        error = error + 1
    else:
        orthologs_error = self.orthologs.validate(logger, path = '.'.join([path, 'orthologs']))
        error = error + orthologs_error
    if self.biological_model is None:
        logger.error("Animal_ModelsEvidence - {0}.biological_model is required".format(path))
        error = error + 1
    elif not isinstance(self.biological_model, evidence_phenotype.Biological_Model):
        logger.error("evidence_phenotype.Biological_Model class instance expected for attribute - {0}.biological_model".format(path))
        error = error + 1
    else:
        biological_model_error = self.biological_model.validate(logger, path = '.'.join([path, 'biological_model']))
        error = error + biological_model_error
    if self.disease_model_association is None:
        logger.error("Animal_ModelsEvidence - {0}.disease_model_association is required".format(path))
        error = error + 1
    elif not isinstance(self.disease_model_association, evidence_phenotype.Disease_Model_Association):
        logger.error("evidence_phenotype.Disease_Model_Association class instance expected for attribute - {0}.disease_model_association".format(path))
        error = error + 1
    else:
        disease_model_association_error = self.disease_model_association.validate(logger, path = '.'.join([path, 'disease_model_association']))
        error = error + disease_model_association_error
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.orthologs is None: classDict['orthologs'] = self.orthologs.serialize()
    if not self.biological_model is None: classDict['biological_model'] = self.biological_model.serialize()
    if not self.disease_model_association is None: classDict['disease_model_association'] = self.disease_model_association.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/drug.json
"""
class Drug(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param drug = None
  :param evidence = None
  :param sourceID = None
  :param access_level = None
  :param validated_against_schema_version = None
  :param unique_association_fields = None
  :param     target = None
  :param     disease = None
  :param     literature = None
  """
  def __init__(self, type = None, drug = None, evidence = None, sourceID = None, access_level = None, validated_against_schema_version = None, unique_association_fields = None,     target = None,     disease = None,     literature = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Drug, self).__init__(sourceID = sourceID,access_level = access_level,validated_against_schema_version = validated_against_schema_version,unique_association_fields = unique_association_fields,target = target,disease = disease,literature = literature)
    
    """
    Name: type
    Type: string
    Required: {True}
    """
    self.type = type
    """
    Name: drug
    """
    self.drug = drug
    """
    Name: evidence
    """
    self.evidence = evidence
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Drug, cls).cloneObject(clone)
    if clone.type:
        obj.type = clone.type
    obj.drug = bioentity.Drug.cloneObject(clone.drug)
    obj.evidence = DrugEvidence.cloneObject(clone.evidence)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['type','drug','evidence','sourceID','access_level','validated_against_schema_version','unique_association_fields','target','disease','literature']
    obj = super(Drug, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Drug - DictType expected - {0} found\n".format(type(map)))
      return
    if  'type' in map:
        obj.type = map['type']
    if  'drug' in map:
        obj.drug = bioentity.Drug.fromMap(map['drug'])
    if  'evidence' in map:
        obj.evidence = DrugEvidence.fromMap(map['evidence'])
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
    if self.sourceID is None:
      logger.error("Drug - {0}.sourceID is required".format(path))
      error = error + 1
    if self.access_level is None:
      logger.error("Drug - {0}.access_level is required".format(path))
      error = error + 1
    if self.validated_against_schema_version is None:
      logger.error("Drug - {0}.validated_against_schema_version is required".format(path))
      error = error + 1
    if self.unique_association_fields is None:
      logger.error("Drug - {0}.unique_association_fields is required".format(path))
      error = error + 1
    if self.target is None:
      logger.error("Drug - {0}.target is required".format(path))
      error = error + 1
    if self.disease is None:
      logger.error("Drug - {0}.disease is required".format(path))
      error = error + 1
    # type is mandatory
    if self.type is None :
        logger.error("Drug - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['known_drug']:
        logger.error("Drug - {0}.type value is restricted to the fixed set of values 'known_drug' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type and not isinstance(self.type, basestring):
        logger.error("Drug - {0}.type type should be a string".format(path))
        error = error + 1
    if self.drug is None:
        logger.error("Drug - {0}.drug is required".format(path))
        error = error + 1
    elif not isinstance(self.drug, bioentity.Drug):
        logger.error("bioentity.Drug class instance expected for attribute - {0}.drug".format(path))
        error = error + 1
    else:
        drug_error = self.drug.validate(logger, path = '.'.join([path, 'drug']))
        error = error + drug_error
    if self.evidence is None:
        logger.error("Drug - {0}.evidence is required".format(path))
        error = error + 1
    elif not isinstance(self.evidence, DrugEvidence):
        logger.error("DrugEvidence class instance expected for attribute - {0}.evidence".format(path))
        error = error + 1
    else:
        evidence_error = self.evidence.validate(logger, path = '.'.join([path, 'evidence']))
        error = error + evidence_error
    return error
  
  def serialize(self):
    classDict = super(Drug, self).serialize()
    if not self.type is None: classDict['type'] = self.type
    if not self.drug is None: classDict['drug'] = self.drug.serialize()
    if not self.evidence is None: classDict['evidence'] = self.evidence.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/drug.json inner class:(evidence)
"""
class DrugEvidence(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param target2drug = None
  :param drug2clinic = None
  """
  def __init__(self, target2drug = None, drug2clinic = None):
    """
    Name: target2drug
    """
    self.target2drug = target2drug
    """
    Name: drug2clinic
    """
    self.drug2clinic = drug2clinic
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    obj.target2drug = evidence_drug.Target2Drug.cloneObject(clone.target2drug)
    obj.drug2clinic = evidence_drug.Drug2Clinic.cloneObject(clone.drug2clinic)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['target2drug','drug2clinic']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("DrugEvidence - DictType expected - {0} found\n".format(type(map)))
      return
    if  'target2drug' in map:
        obj.target2drug = evidence_drug.Target2Drug.fromMap(map['target2drug'])
    if  'drug2clinic' in map:
        obj.drug2clinic = evidence_drug.Drug2Clinic.fromMap(map['drug2clinic'])
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class DrugEvidence
    :returns: number of errors found during validation
    """
    error = 0
    if self.target2drug is None:
        logger.error("DrugEvidence - {0}.target2drug is required".format(path))
        error = error + 1
    elif not isinstance(self.target2drug, evidence_drug.Target2Drug):
        logger.error("evidence_drug.Target2Drug class instance expected for attribute - {0}.target2drug".format(path))
        error = error + 1
    else:
        target2drug_error = self.target2drug.validate(logger, path = '.'.join([path, 'target2drug']))
        error = error + target2drug_error
    if self.drug2clinic is None:
        logger.error("DrugEvidence - {0}.drug2clinic is required".format(path))
        error = error + 1
    elif not isinstance(self.drug2clinic, evidence_drug.Drug2Clinic):
        logger.error("evidence_drug.Drug2Clinic class instance expected for attribute - {0}.drug2clinic".format(path))
        error = error + 1
    else:
        drug2clinic_error = self.drug2clinic.validate(logger, path = '.'.join([path, 'drug2clinic']))
        error = error + drug2clinic_error
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.target2drug is None: classDict['target2drug'] = self.target2drug.serialize()
    if not self.drug2clinic is None: classDict['drug2clinic'] = self.drug2clinic.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/expression.json
"""
class Expression(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param evidence = None
  :param sourceID = None
  :param access_level = None
  :param validated_against_schema_version = None
  :param unique_association_fields = None
  :param     target = None
  :param     disease = None
  :param     literature = None
  """
  def __init__(self, type = None, evidence = None, sourceID = None, access_level = None, validated_against_schema_version = None, unique_association_fields = None,     target = None,     disease = None,     literature = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Expression, self).__init__(sourceID = sourceID,access_level = access_level,validated_against_schema_version = validated_against_schema_version,unique_association_fields = unique_association_fields,target = target,disease = disease,literature = literature)
    
    """
    Name: type
    Type: string
    Required: {True}
    """
    self.type = type
    """
    Name: evidence
    """
    self.evidence = evidence
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Expression, cls).cloneObject(clone)
    if clone.type:
        obj.type = clone.type
    obj.evidence = evidence_core.Expression.cloneObject(clone.evidence)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['type','evidence','sourceID','access_level','validated_against_schema_version','unique_association_fields','target','disease','literature']
    obj = super(Expression, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Expression - DictType expected - {0} found\n".format(type(map)))
      return
    if  'type' in map:
        obj.type = map['type']
    if  'evidence' in map:
        obj.evidence = evidence_core.Expression.fromMap(map['evidence'])
    for key in map:
      if not key in cls_keys:
        logger.warn("Expression - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Expression
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Expression, self).validate(logger, path = path)
    if self.sourceID is None:
      logger.error("Expression - {0}.sourceID is required".format(path))
      error = error + 1
    if self.access_level is None:
      logger.error("Expression - {0}.access_level is required".format(path))
      error = error + 1
    if self.validated_against_schema_version is None:
      logger.error("Expression - {0}.validated_against_schema_version is required".format(path))
      error = error + 1
    if self.unique_association_fields is None:
      logger.error("Expression - {0}.unique_association_fields is required".format(path))
      error = error + 1
    if self.target is None:
      logger.error("Expression - {0}.target is required".format(path))
      error = error + 1
    if self.disease is None:
      logger.error("Expression - {0}.disease is required".format(path))
      error = error + 1
    # type is mandatory
    if self.type is None :
        logger.error("Expression - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['rna_expression']:
        logger.error("Expression - {0}.type value is restricted to the fixed set of values 'rna_expression' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type and not isinstance(self.type, basestring):
        logger.error("Expression - {0}.type type should be a string".format(path))
        error = error + 1
    if self.evidence is None:
        logger.error("Expression - {0}.evidence is required".format(path))
        error = error + 1
    elif not isinstance(self.evidence, evidence_core.Expression):
        logger.error("evidence_core.Expression class instance expected for attribute - {0}.evidence".format(path))
        error = error + 1
    else:
        evidence_error = self.evidence.validate(logger, path = '.'.join([path, 'evidence']))
        error = error + evidence_error
    return error
  
  def serialize(self):
    classDict = super(Expression, self).serialize()
    if not self.type is None: classDict['type'] = self.type
    if not self.evidence is None: classDict['evidence'] = self.evidence.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/genetics.json
"""
class Genetics(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param variant = None
  :param evidence = None
  :param sourceID = None
  :param access_level = None
  :param validated_against_schema_version = None
  :param unique_association_fields = None
  :param     target = None
  :param     disease = None
  :param     literature = None
  """
  def __init__(self, type = None, variant = None, evidence = None, sourceID = None, access_level = None, validated_against_schema_version = None, unique_association_fields = None,     target = None,     disease = None,     literature = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Genetics, self).__init__(sourceID = sourceID,access_level = access_level,validated_against_schema_version = validated_against_schema_version,unique_association_fields = unique_association_fields,target = target,disease = disease,literature = literature)
    
    """
    Name: type
    Type: string
    Required: {True}
    """
    self.type = type
    """
    Name: variant
    """
    self.variant = variant
    """
    Name: evidence
    """
    self.evidence = evidence
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Genetics, cls).cloneObject(clone)
    if clone.type:
        obj.type = clone.type
    obj.variant = bioentity.Variant.cloneObject(clone.variant)
    obj.evidence = GeneticsEvidence.cloneObject(clone.evidence)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['type','variant','evidence','sourceID','access_level','validated_against_schema_version','unique_association_fields','target','disease','literature']
    obj = super(Genetics, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Genetics - DictType expected - {0} found\n".format(type(map)))
      return
    if  'type' in map:
        obj.type = map['type']
    if  'variant' in map:
        obj.variant = bioentity.Variant.fromMap(map['variant'])
    if  'evidence' in map:
        obj.evidence = GeneticsEvidence.fromMap(map['evidence'])
    for key in map:
      if not key in cls_keys:
        logger.warn("Genetics - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Genetics
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Genetics, self).validate(logger, path = path)
    if self.sourceID is None:
      logger.error("Genetics - {0}.sourceID is required".format(path))
      error = error + 1
    if self.access_level is None:
      logger.error("Genetics - {0}.access_level is required".format(path))
      error = error + 1
    if self.validated_against_schema_version is None:
      logger.error("Genetics - {0}.validated_against_schema_version is required".format(path))
      error = error + 1
    if self.unique_association_fields is None:
      logger.error("Genetics - {0}.unique_association_fields is required".format(path))
      error = error + 1
    if self.target is None:
      logger.error("Genetics - {0}.target is required".format(path))
      error = error + 1
    if self.disease is None:
      logger.error("Genetics - {0}.disease is required".format(path))
      error = error + 1
    # type is mandatory
    if self.type is None :
        logger.error("Genetics - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['genetic_association']:
        logger.error("Genetics - {0}.type value is restricted to the fixed set of values 'genetic_association' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type and not isinstance(self.type, basestring):
        logger.error("Genetics - {0}.type type should be a string".format(path))
        error = error + 1
    if self.variant is None:
        logger.error("Genetics - {0}.variant is required".format(path))
        error = error + 1
    elif not isinstance(self.variant, bioentity.Variant):
        logger.error("bioentity.Variant class instance expected for attribute - {0}.variant".format(path))
        error = error + 1
    else:
        variant_error = self.variant.validate(logger, path = '.'.join([path, 'variant']))
        error = error + variant_error
    if self.evidence is None:
        logger.error("Genetics - {0}.evidence is required".format(path))
        error = error + 1
    elif not isinstance(self.evidence, GeneticsEvidence):
        logger.error("GeneticsEvidence class instance expected for attribute - {0}.evidence".format(path))
        error = error + 1
    else:
        evidence_error = self.evidence.validate(logger, path = '.'.join([path, 'evidence']))
        error = error + evidence_error
    return error
  
  def serialize(self):
    classDict = super(Genetics, self).serialize()
    if not self.type is None: classDict['type'] = self.type
    if not self.variant is None: classDict['variant'] = self.variant.serialize()
    if not self.evidence is None: classDict['evidence'] = self.evidence.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/genetics.json inner class:(evidence)
"""
class GeneticsEvidence(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param gene2variant = None
  :param variant2disease = None
  """
  def __init__(self, gene2variant = None, variant2disease = None):
    """
    Name: gene2variant
    """
    self.gene2variant = gene2variant
    """
    Name: variant2disease
    """
    self.variant2disease = variant2disease
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    obj.gene2variant = evidence_genetics.Gene2Variant.cloneObject(clone.gene2variant)
    obj.variant2disease = evidence_genetics.Variant2Disease.cloneObject(clone.variant2disease)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['gene2variant','variant2disease']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("GeneticsEvidence - DictType expected - {0} found\n".format(type(map)))
      return
    if  'gene2variant' in map:
        obj.gene2variant = evidence_genetics.Gene2Variant.fromMap(map['gene2variant'])
    if  'variant2disease' in map:
        obj.variant2disease = evidence_genetics.Variant2Disease.fromMap(map['variant2disease'])
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class GeneticsEvidence
    :returns: number of errors found during validation
    """
    error = 0
    if self.gene2variant is None:
        logger.error("GeneticsEvidence - {0}.gene2variant is required".format(path))
        error = error + 1
    elif not isinstance(self.gene2variant, evidence_genetics.Gene2Variant):
        logger.error("evidence_genetics.Gene2Variant class instance expected for attribute - {0}.gene2variant".format(path))
        error = error + 1
    else:
        gene2variant_error = self.gene2variant.validate(logger, path = '.'.join([path, 'gene2variant']))
        error = error + gene2variant_error
    if self.variant2disease is None:
        logger.error("GeneticsEvidence - {0}.variant2disease is required".format(path))
        error = error + 1
    elif not isinstance(self.variant2disease, evidence_genetics.Variant2Disease):
        logger.error("evidence_genetics.Variant2Disease class instance expected for attribute - {0}.variant2disease".format(path))
        error = error + 1
    else:
        variant2disease_error = self.variant2disease.validate(logger, path = '.'.join([path, 'variant2disease']))
        error = error + variant2disease_error
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.gene2variant is None: classDict['gene2variant'] = self.gene2variant.serialize()
    if not self.variant2disease is None: classDict['variant2disease'] = self.variant2disease.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/literature_curated.json
"""
class Literature_Curated(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param evidence = None
  :param sourceID = None
  :param access_level = None
  :param validated_against_schema_version = None
  :param unique_association_fields = None
  :param     target = None
  :param     disease = None
  :param     literature = None
  """
  def __init__(self, type = None, evidence = None, sourceID = None, access_level = None, validated_against_schema_version = None, unique_association_fields = None,     target = None,     disease = None,     literature = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Literature_Curated, self).__init__(sourceID = sourceID,access_level = access_level,validated_against_schema_version = validated_against_schema_version,unique_association_fields = unique_association_fields,target = target,disease = disease,literature = literature)
    
    """
    Name: type
    Type: string
    Required: {True}
    """
    self.type = type
    """
    Name: evidence
    """
    self.evidence = evidence
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Literature_Curated, cls).cloneObject(clone)
    if clone.type:
        obj.type = clone.type
    obj.evidence = evidence_core.Literature_Curated.cloneObject(clone.evidence)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['type','evidence','sourceID','access_level','validated_against_schema_version','unique_association_fields','target','disease','literature']
    obj = super(Literature_Curated, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Literature_Curated - DictType expected - {0} found\n".format(type(map)))
      return
    if  'type' in map:
        obj.type = map['type']
    if  'evidence' in map:
        obj.evidence = evidence_core.Literature_Curated.fromMap(map['evidence'])
    for key in map:
      if not key in cls_keys:
        logger.warn("Literature_Curated - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Literature_Curated
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Literature_Curated, self).validate(logger, path = path)
    if self.sourceID is None:
      logger.error("Literature_Curated - {0}.sourceID is required".format(path))
      error = error + 1
    if self.access_level is None:
      logger.error("Literature_Curated - {0}.access_level is required".format(path))
      error = error + 1
    if self.validated_against_schema_version is None:
      logger.error("Literature_Curated - {0}.validated_against_schema_version is required".format(path))
      error = error + 1
    if self.unique_association_fields is None:
      logger.error("Literature_Curated - {0}.unique_association_fields is required".format(path))
      error = error + 1
    if self.target is None:
      logger.error("Literature_Curated - {0}.target is required".format(path))
      error = error + 1
    if self.disease is None:
      logger.error("Literature_Curated - {0}.disease is required".format(path))
      error = error + 1
    # type is mandatory
    if self.type is None :
        logger.error("Literature_Curated - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['genetic_literature','affected_pathway','somatic_mutation']:
        logger.error("Literature_Curated - {0}.type value is restricted to the fixed set of values 'genetic_literature','affected_pathway','somatic_mutation' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type and not isinstance(self.type, basestring):
        logger.error("Literature_Curated - {0}.type type should be a string".format(path))
        error = error + 1
    if self.evidence is None:
        logger.error("Literature_Curated - {0}.evidence is required".format(path))
        error = error + 1
    elif not isinstance(self.evidence, evidence_core.Literature_Curated):
        logger.error("evidence_core.Literature_Curated class instance expected for attribute - {0}.evidence".format(path))
        error = error + 1
    else:
        evidence_error = self.evidence.validate(logger, path = '.'.join([path, 'evidence']))
        error = error + evidence_error
    return error
  
  def serialize(self):
    classDict = super(Literature_Curated, self).serialize()
    if not self.type is None: classDict['type'] = self.type
    if not self.evidence is None: classDict['evidence'] = self.evidence.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/literature_mining.json
"""
class Literature_Mining(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param type = None
  :param evidence = None
  :param sourceID = None
  :param access_level = None
  :param validated_against_schema_version = None
  :param unique_association_fields = None
  :param     target = None
  :param     disease = None
  :param     literature = None
  """
  def __init__(self, type = None, evidence = None, sourceID = None, access_level = None, validated_against_schema_version = None, unique_association_fields = None,     target = None,     disease = None,     literature = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Literature_Mining, self).__init__(sourceID = sourceID,access_level = access_level,validated_against_schema_version = validated_against_schema_version,unique_association_fields = unique_association_fields,target = target,disease = disease,literature = literature)
    
    """
    Name: type
    Type: string
    Required: {True}
    """
    self.type = type
    """
    Name: evidence
    """
    self.evidence = evidence
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Literature_Mining, cls).cloneObject(clone)
    if clone.type:
        obj.type = clone.type
    obj.evidence = evidence_core.Literature_Mining.cloneObject(clone.evidence)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['type','evidence','sourceID','access_level','validated_against_schema_version','unique_association_fields','target','disease','literature']
    obj = super(Literature_Mining, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Literature_Mining - DictType expected - {0} found\n".format(type(map)))
      return
    if  'type' in map:
        obj.type = map['type']
    if  'evidence' in map:
        obj.evidence = evidence_core.Literature_Mining.fromMap(map['evidence'])
    for key in map:
      if not key in cls_keys:
        logger.warn("Literature_Mining - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Literature_Mining
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Literature_Mining, self).validate(logger, path = path)
    if self.sourceID is None:
      logger.error("Literature_Mining - {0}.sourceID is required".format(path))
      error = error + 1
    if self.access_level is None:
      logger.error("Literature_Mining - {0}.access_level is required".format(path))
      error = error + 1
    if self.validated_against_schema_version is None:
      logger.error("Literature_Mining - {0}.validated_against_schema_version is required".format(path))
      error = error + 1
    if self.unique_association_fields is None:
      logger.error("Literature_Mining - {0}.unique_association_fields is required".format(path))
      error = error + 1
    if self.target is None:
      logger.error("Literature_Mining - {0}.target is required".format(path))
      error = error + 1
    if self.disease is None:
      logger.error("Literature_Mining - {0}.disease is required".format(path))
      error = error + 1
    # type is mandatory
    if self.type is None :
        logger.error("Literature_Mining - {0}.type is required".format(path))
        error = error + 1
    if not self.type is None and not self.type in ['literature']:
        logger.error("Literature_Mining - {0}.type value is restricted to the fixed set of values 'literature' ('{1}' given)".format(path, self.type))
        error = error + 1
    if self.type and not isinstance(self.type, basestring):
        logger.error("Literature_Mining - {0}.type type should be a string".format(path))
        error = error + 1
    if self.evidence is None:
        logger.error("Literature_Mining - {0}.evidence is required".format(path))
        error = error + 1
    elif not isinstance(self.evidence, evidence_core.Literature_Mining):
        logger.error("evidence_core.Literature_Mining class instance expected for attribute - {0}.evidence".format(path))
        error = error + 1
    else:
        evidence_error = self.evidence.validate(logger, path = '.'.join([path, 'evidence']))
        error = error + evidence_error
    return error
  
  def serialize(self):
    classDict = super(Literature_Mining, self).serialize()
    if not self.type is None: classDict['type'] = self.type
    if not self.evidence is None: classDict['evidence'] = self.evidence.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
