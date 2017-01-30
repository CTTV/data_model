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
import opentargets.model.evidence.core
import opentargets.model.evidence.linkout as evidence_linkout
import opentargets.model.bioentity as bioentity

__author__ = "Gautier Koscielny"
__copyright__ = "Copyright 2014-2017, Open Targets"
__credits__ = ["Gautier Koscielny", "Samiul Hasan"]
__license__ = "Apache 2.0"
__version__ = "1.2.4"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautierk@targetvalidation.org"
__status__ = "Production"

logger = logging.getLogger(__name__)
import opentargets.model.evidence.core as evidence_core
"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/phenotype/orthologs.json
"""
class Orthologs(evidence_core.Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param evidence_codes = None
  :param human_gene_id = None
  :param model_gene_id = None
  :param urls = None
  :param species = None
  :param unique_experiment_reference = None
  :param     provenance_type = None
  :param is_associated = False
  :param resource_score = None
  :param date_asserted = None
  """
  def __init__(self, evidence_codes = None, human_gene_id = None, model_gene_id = None, urls = None, species = None, unique_experiment_reference = None,     provenance_type = None, is_associated = False, resource_score = None, date_asserted = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Orthologs, self).__init__(unique_experiment_reference = unique_experiment_reference,provenance_type = provenance_type,is_associated = is_associated,resource_score = resource_score,date_asserted = date_asserted)
    
    """
    Name: evidence_codes
    Type: array
    Description: An array of evidence codes
    Required: {True}
    """
    self.evidence_codes = evidence_codes
    
    """
    Name: human_gene_id
    Type: string
    Description: Human Ensembl gene identifier
    Required: {True}
    """
    self.human_gene_id = human_gene_id
    
    """
    Name: model_gene_id
    Type: string
    Description: Biological model Ensembl gene identifier (ortholog)
    Required: {True}
    """
    self.model_gene_id = model_gene_id
    
    """
    Name: urls
    Type: array
    """
    self.urls = urls
    
    """
    Name: species
    Type: string
    Required: {True}
    """
    self.species = species
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Orthologs, cls).cloneObject(clone)
    if clone.evidence_codes:
        obj.evidence_codes = []; obj.evidence_codes.extend(clone.evidence_codes)
    if clone.human_gene_id:
        obj.human_gene_id = clone.human_gene_id
    if clone.model_gene_id:
        obj.model_gene_id = clone.model_gene_id
    if clone.urls:
        obj.urls = []; obj.urls.extend(clone.urls)
    if clone.species:
        obj.species = clone.species
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['evidence_codes','human_gene_id','model_gene_id','urls','species','unique_experiment_reference','provenance_type','is_associated','resource_score','date_asserted']
    obj = super(Orthologs, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Orthologs - DictType expected - {0} found\n".format(type(map)))
      return
    if  'evidence_codes' in map:
        obj.evidence_codes = map['evidence_codes']
    if  'human_gene_id' in map:
        obj.human_gene_id = map['human_gene_id']
    if  'model_gene_id' in map:
        obj.model_gene_id = map['model_gene_id']
    if 'urls' in map and isinstance(map['urls'], list):
        obj.urls = []
        for item in map['urls']:
            obj.urls.append(evidence_linkout.Linkout.fromMap(item))
    if  'species' in map:
        obj.species = map['species']
    for key in map:
      if not key in cls_keys:
        logger.warn("Orthologs - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Orthologs
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Orthologs, self).validate(logger, path = path)
    if self.provenance_type is None:
      logger.error("Orthologs - {0}.provenance_type is required".format(path))
      error = error + 1
    if self.is_associated is None:
      logger.error("Orthologs - {0}.is_associated is required".format(path))
      error = error + 1
    if self.resource_score is None:
      logger.error("Orthologs - {0}.resource_score is required".format(path))
      error = error + 1
    if self.date_asserted is None:
      logger.error("Orthologs - {0}.date_asserted is required".format(path))
      error = error + 1
    # evidence_codes is mandatory
    if self.evidence_codes is None :
        logger.error("Orthologs - {0}.evidence_codes is required".format(path))
        error = error + 1
    if not self.evidence_codes is None:
        validValues = ['http://identifiers.org/eco/ECO:0000265']
        for item in self.evidence_codes:
            if item not in validValues:
                logger.error("Orthologs - {0}.evidence_codes value is restricted to the fixed set of values 'http://identifiers.org/eco/ECO:0000265' ('{1}' given)".format(path, item))
                error = error + 1
    if not self.evidence_codes is None and len(self.evidence_codes) > 0 and not all(isinstance(n, basestring) for n in self.evidence_codes):
        logger.error("Orthologs - {0}.evidence_codes array should have elements of type 'basestring'".format(path))
        error = error+1
    if self.evidence_codes and len(self.evidence_codes) < 1:
        logger.error("Orthologs - {0}.evidence_codes array should have at least 1 elements".format(path))
        error = error + 1
    # human_gene_id is mandatory
    if self.human_gene_id is None :
        logger.error("Orthologs - {0}.human_gene_id is required".format(path))
        error = error + 1
    """ Check regex: ^http://identifiers.org/ensembl/ENSG[0-9]{4,}$ for validation"""
    if self.human_gene_id and not re.match('^http://identifiers.org/ensembl/ENSG[0-9]{4,}$', self.human_gene_id):
        logger.error("Orthologs - {0}.human_gene_id '{1}'".format(path,self.human_gene_id) + " does not match pattern '^http://identifiers.org/ensembl/ENSG[0-9]{4,}$'")
        logger.warn(json.dumps(self.human_gene_id, sort_keys=True, indent=2))
    if self.human_gene_id and not isinstance(self.human_gene_id, basestring):
        logger.error("Orthologs - {0}.human_gene_id type should be a string".format(path))
        error = error + 1
    # model_gene_id is mandatory
    if self.model_gene_id is None :
        logger.error("Orthologs - {0}.model_gene_id is required".format(path))
        error = error + 1
    """ Check regex: ^http://identifiers.org/ensembl/ENS[A-Z]{0,3}G[0-9]{4,}$ for validation"""
    if self.model_gene_id and not re.match('^http://identifiers.org/ensembl/ENS[A-Z]{0,3}G[0-9]{4,}$', self.model_gene_id):
        logger.error("Orthologs - {0}.model_gene_id '{1}'".format(path,self.model_gene_id) + " does not match pattern '^http://identifiers.org/ensembl/ENS[A-Z]{0,3}G[0-9]{4,}$'")
        logger.warn(json.dumps(self.model_gene_id, sort_keys=True, indent=2))
    if self.model_gene_id and not isinstance(self.model_gene_id, basestring):
        logger.error("Orthologs - {0}.model_gene_id type should be a string".format(path))
        error = error + 1
    if not self.urls is None and len(self.urls) > 0 and not all(isinstance(n, evidence_linkout.Linkout) for n in self.urls):
        logger.error("Orthologs - {0}.urls array should have elements of type 'evidence_linkout.Linkout'".format(path))
        error = error+1
    # species is mandatory
    if self.species is None :
        logger.error("Orthologs - {0}.species is required".format(path))
        error = error + 1
    if not self.species is None and not self.species in ['mouse','human','rat','zebrafish','dog']:
        logger.error("Orthologs - {0}.species value is restricted to the fixed set of values 'mouse','human','rat','zebrafish','dog' ('{1}' given)".format(path, self.species))
        error = error + 1
    if self.species and not isinstance(self.species, basestring):
        logger.error("Orthologs - {0}.species type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = super(Orthologs, self).serialize()
    if not self.evidence_codes is None: classDict['evidence_codes'] = self.evidence_codes
    if not self.human_gene_id is None: classDict['human_gene_id'] = self.human_gene_id
    if not self.model_gene_id is None: classDict['model_gene_id'] = self.model_gene_id
    if not self.urls is None: classDict['urls'] = map(lambda x: x.serialize(), self.urls)
    if not self.species is None: classDict['species'] = self.species
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
import opentargets.model.evidence.core as evidence_core
"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/phenotype/biological_model.json
"""
class Biological_Model(evidence_core.Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param model_id = None
  :param allele_ids = None
  :param zygosity = None
  :param phenotypes = None
  :param genetic_background = None
  :param allelic_composition = None
  :param model_gene_id = None
  :param urls = None
  :param species = None
  :param evidence_codes = None
  :param unique_experiment_reference = None
  :param     provenance_type = None
  :param is_associated = False
  :param resource_score = None
  :param date_asserted = None
  """
  def __init__(self, model_id = None, allele_ids = None, zygosity = None, phenotypes = None, genetic_background = None, allelic_composition = None, model_gene_id = None, urls = None, species = None, evidence_codes = None, unique_experiment_reference = None,     provenance_type = None, is_associated = False, resource_score = None, date_asserted = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Biological_Model, self).__init__(unique_experiment_reference = unique_experiment_reference,provenance_type = provenance_type,is_associated = is_associated,resource_score = resource_score,date_asserted = date_asserted)
    
    """
    Name: model_id
    Type: string
    Description: Internal identifier for the biological model
    Required: {True}
    """
    self.model_id = model_id
    
    """
    Name: allele_ids
    Type: string
    Description: List of allele identifiers for this model separated by |
    Required: {True}
    """
    self.allele_ids = allele_ids
    
    """
    Name: zygosity
    Type: string
    Required: {True}
    """
    self.zygosity = zygosity
    
    """
    Name: phenotypes
    Type: array
    Description: List of phenotypes for this model
    Required: {True}
    """
    self.phenotypes = phenotypes
    
    """
    Name: genetic_background
    Type: string
    Description: Genetic background of the biological model that influences phenotypes
    Required: {True}
    """
    self.genetic_background = genetic_background
    
    """
    Name: allelic_composition
    Type: string
    Description: Animal model allelic composition
    Required: {True}
    """
    self.allelic_composition = allelic_composition
    
    """
    Name: model_gene_id
    Type: string
    Description: Biological model Ensembl gene identifier (ortholog)
    Required: {True}
    """
    self.model_gene_id = model_gene_id
    
    """
    Name: urls
    Type: array
    """
    self.urls = urls
    
    """
    Name: species
    Type: string
    Required: {True}
    """
    self.species = species
    
    """
    Name: evidence_codes
    Type: array
    Description: An array of evidence codes
    Required: {True}
    """
    self.evidence_codes = evidence_codes
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Biological_Model, cls).cloneObject(clone)
    if clone.model_id:
        obj.model_id = clone.model_id
    if clone.allele_ids:
        obj.allele_ids = clone.allele_ids
    if clone.zygosity:
        obj.zygosity = clone.zygosity
    if clone.phenotypes:
        obj.phenotypes = []; obj.phenotypes.extend(clone.phenotypes)
    if clone.genetic_background:
        obj.genetic_background = clone.genetic_background
    if clone.allelic_composition:
        obj.allelic_composition = clone.allelic_composition
    if clone.model_gene_id:
        obj.model_gene_id = clone.model_gene_id
    if clone.urls:
        obj.urls = []; obj.urls.extend(clone.urls)
    if clone.species:
        obj.species = clone.species
    if clone.evidence_codes:
        obj.evidence_codes = []; obj.evidence_codes.extend(clone.evidence_codes)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['model_id','allele_ids','zygosity','phenotypes','genetic_background','allelic_composition','model_gene_id','urls','species','evidence_codes','unique_experiment_reference','provenance_type','is_associated','resource_score','date_asserted']
    obj = super(Biological_Model, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Biological_Model - DictType expected - {0} found\n".format(type(map)))
      return
    if  'model_id' in map:
        obj.model_id = map['model_id']
    if  'allele_ids' in map:
        obj.allele_ids = map['allele_ids']
    if  'zygosity' in map:
        obj.zygosity = map['zygosity']
    if 'phenotypes' in map and isinstance(map['phenotypes'], list):
        obj.phenotypes = []
        for item in map['phenotypes']:
            obj.phenotypes.append(bioentity.Phenotype.fromMap(item))
    if  'genetic_background' in map:
        obj.genetic_background = map['genetic_background']
    if  'allelic_composition' in map:
        obj.allelic_composition = map['allelic_composition']
    if  'model_gene_id' in map:
        obj.model_gene_id = map['model_gene_id']
    if 'urls' in map and isinstance(map['urls'], list):
        obj.urls = []
        for item in map['urls']:
            obj.urls.append(evidence_linkout.Linkout.fromMap(item))
    if  'species' in map:
        obj.species = map['species']
    if  'evidence_codes' in map:
        obj.evidence_codes = map['evidence_codes']
    for key in map:
      if not key in cls_keys:
        logger.warn("Biological_Model - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Biological_Model
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Biological_Model, self).validate(logger, path = path)
    if self.provenance_type is None:
      logger.error("Biological_Model - {0}.provenance_type is required".format(path))
      error = error + 1
    if self.is_associated is None:
      logger.error("Biological_Model - {0}.is_associated is required".format(path))
      error = error + 1
    if self.resource_score is None:
      logger.error("Biological_Model - {0}.resource_score is required".format(path))
      error = error + 1
    if self.date_asserted is None:
      logger.error("Biological_Model - {0}.date_asserted is required".format(path))
      error = error + 1
    # model_id is mandatory
    if self.model_id is None :
        logger.error("Biological_Model - {0}.model_id is required".format(path))
        error = error + 1
    if self.model_id and not isinstance(self.model_id, basestring):
        logger.error("Biological_Model - {0}.model_id type should be a string".format(path))
        error = error + 1
    # allele_ids is mandatory
    if self.allele_ids is None :
        logger.error("Biological_Model - {0}.allele_ids is required".format(path))
        error = error + 1
    if self.allele_ids and not isinstance(self.allele_ids, basestring):
        logger.error("Biological_Model - {0}.allele_ids type should be a string".format(path))
        error = error + 1
    # zygosity is mandatory
    if self.zygosity is None :
        logger.error("Biological_Model - {0}.zygosity is required".format(path))
        error = error + 1
    if not self.zygosity is None and not self.zygosity in ['hom','het','hem','oth']:
        logger.error("Biological_Model - {0}.zygosity value is restricted to the fixed set of values 'hom','het','hem','oth' ('{1}' given)".format(path, self.zygosity))
        error = error + 1
    if self.zygosity and not isinstance(self.zygosity, basestring):
        logger.error("Biological_Model - {0}.zygosity type should be a string".format(path))
        error = error + 1
    # phenotypes is mandatory
    if self.phenotypes is None :
        logger.error("Biological_Model - {0}.phenotypes is required".format(path))
        error = error + 1
    if not self.phenotypes is None and len(self.phenotypes) > 0 and not all(isinstance(n, bioentity.Phenotype) for n in self.phenotypes):
        logger.error("Biological_Model - {0}.phenotypes array should have elements of type 'bioentity.Phenotype'".format(path))
        error = error+1
    if self.phenotypes and len(self.phenotypes) < 1:
        logger.error("Biological_Model - {0}.phenotypes array should have at least 1 elements".format(path))
        error = error + 1
    # genetic_background is mandatory
    if self.genetic_background is None :
        logger.error("Biological_Model - {0}.genetic_background is required".format(path))
        error = error + 1
    if self.genetic_background and not isinstance(self.genetic_background, basestring):
        logger.error("Biological_Model - {0}.genetic_background type should be a string".format(path))
        error = error + 1
    # allelic_composition is mandatory
    if self.allelic_composition is None :
        logger.error("Biological_Model - {0}.allelic_composition is required".format(path))
        error = error + 1
    if self.allelic_composition and not isinstance(self.allelic_composition, basestring):
        logger.error("Biological_Model - {0}.allelic_composition type should be a string".format(path))
        error = error + 1
    # model_gene_id is mandatory
    if self.model_gene_id is None :
        logger.error("Biological_Model - {0}.model_gene_id is required".format(path))
        error = error + 1
    """ Check regex: ^http://identifiers.org/ensembl/ENS[A-Z]{0,3}G[0-9]{4,}$ for validation"""
    if self.model_gene_id and not re.match('^http://identifiers.org/ensembl/ENS[A-Z]{0,3}G[0-9]{4,}$', self.model_gene_id):
        logger.error("Biological_Model - {0}.model_gene_id '{1}'".format(path,self.model_gene_id) + " does not match pattern '^http://identifiers.org/ensembl/ENS[A-Z]{0,3}G[0-9]{4,}$'")
        logger.warn(json.dumps(self.model_gene_id, sort_keys=True, indent=2))
    if self.model_gene_id and not isinstance(self.model_gene_id, basestring):
        logger.error("Biological_Model - {0}.model_gene_id type should be a string".format(path))
        error = error + 1
    if not self.urls is None and len(self.urls) > 0 and not all(isinstance(n, evidence_linkout.Linkout) for n in self.urls):
        logger.error("Biological_Model - {0}.urls array should have elements of type 'evidence_linkout.Linkout'".format(path))
        error = error+1
    # species is mandatory
    if self.species is None :
        logger.error("Biological_Model - {0}.species is required".format(path))
        error = error + 1
    if not self.species is None and not self.species in ['mouse','human','rat','zebrafish','dog']:
        logger.error("Biological_Model - {0}.species value is restricted to the fixed set of values 'mouse','human','rat','zebrafish','dog' ('{1}' given)".format(path, self.species))
        error = error + 1
    if self.species and not isinstance(self.species, basestring):
        logger.error("Biological_Model - {0}.species type should be a string".format(path))
        error = error + 1
    # evidence_codes is mandatory
    if self.evidence_codes is None :
        logger.error("Biological_Model - {0}.evidence_codes is required".format(path))
        error = error + 1
    if not self.evidence_codes is None:
        validValues = ['http://identifiers.org/eco/ECO:0000179']
        for item in self.evidence_codes:
            if item not in validValues:
                logger.error("Biological_Model - {0}.evidence_codes value is restricted to the fixed set of values 'http://identifiers.org/eco/ECO:0000179' ('{1}' given)".format(path, item))
                error = error + 1
    if not self.evidence_codes is None and len(self.evidence_codes) > 0 and not all(isinstance(n, basestring) for n in self.evidence_codes):
        logger.error("Biological_Model - {0}.evidence_codes array should have elements of type 'basestring'".format(path))
        error = error+1
    if self.evidence_codes and len(self.evidence_codes) < 1:
        logger.error("Biological_Model - {0}.evidence_codes array should have at least 1 elements".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = super(Biological_Model, self).serialize()
    if not self.model_id is None: classDict['model_id'] = self.model_id
    if not self.allele_ids is None: classDict['allele_ids'] = self.allele_ids
    if not self.zygosity is None: classDict['zygosity'] = self.zygosity
    if not self.phenotypes is None: classDict['phenotypes'] = map(lambda x: x.serialize(), self.phenotypes)
    if not self.genetic_background is None: classDict['genetic_background'] = self.genetic_background
    if not self.allelic_composition is None: classDict['allelic_composition'] = self.allelic_composition
    if not self.model_gene_id is None: classDict['model_gene_id'] = self.model_gene_id
    if not self.urls is None: classDict['urls'] = map(lambda x: x.serialize(), self.urls)
    if not self.species is None: classDict['species'] = self.species
    if not self.evidence_codes is None: classDict['evidence_codes'] = self.evidence_codes
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
import opentargets.model.evidence.core as evidence_core
"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/phenotype/disease_model_association.json
"""
class Disease_Model_Association(evidence_core.Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param model_id = None
  :param model_phenotypes = None
  :param human_phenotypes = None
  :param disease_id = None
  :param urls = None
  :param evidence_codes = None
  :param unique_experiment_reference = None
  :param     provenance_type = None
  :param is_associated = False
  :param resource_score = None
  :param date_asserted = None
  """
  def __init__(self, model_id = None, model_phenotypes = None, human_phenotypes = None, disease_id = None, urls = None, evidence_codes = None, unique_experiment_reference = None,     provenance_type = None, is_associated = False, resource_score = None, date_asserted = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Disease_Model_Association, self).__init__(unique_experiment_reference = unique_experiment_reference,provenance_type = provenance_type,is_associated = is_associated,resource_score = resource_score,date_asserted = date_asserted)
    
    """
    Name: model_id
    Type: string
    Description: Internal identifier for the biological model
    Required: {True}
    """
    self.model_id = model_id
    
    """
    Name: model_phenotypes
    Type: array
    Description: List of biomodel phenotypes for this model
    Required: {True}
    """
    self.model_phenotypes = model_phenotypes
    
    """
    Name: human_phenotypes
    Type: array
    Description: List of human phenotypes for this model
    Required: {True}
    """
    self.human_phenotypes = human_phenotypes
    
    """
    Name: disease_id
    Type: string
    Description: Disease identifier
    Required: {True}
    """
    self.disease_id = disease_id
    
    """
    Name: urls
    Type: array
    """
    self.urls = urls
    
    """
    Name: evidence_codes
    Type: array
    Description: An array of evidence codes
    Required: {True}
    """
    self.evidence_codes = evidence_codes
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Disease_Model_Association, cls).cloneObject(clone)
    if clone.model_id:
        obj.model_id = clone.model_id
    if clone.model_phenotypes:
        obj.model_phenotypes = []; obj.model_phenotypes.extend(clone.model_phenotypes)
    if clone.human_phenotypes:
        obj.human_phenotypes = []; obj.human_phenotypes.extend(clone.human_phenotypes)
    if clone.disease_id:
        obj.disease_id = clone.disease_id
    if clone.urls:
        obj.urls = []; obj.urls.extend(clone.urls)
    if clone.evidence_codes:
        obj.evidence_codes = []; obj.evidence_codes.extend(clone.evidence_codes)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['model_id','model_phenotypes','human_phenotypes','disease_id','urls','evidence_codes','unique_experiment_reference','provenance_type','is_associated','resource_score','date_asserted']
    obj = super(Disease_Model_Association, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Disease_Model_Association - DictType expected - {0} found\n".format(type(map)))
      return
    if  'model_id' in map:
        obj.model_id = map['model_id']
    if 'model_phenotypes' in map and isinstance(map['model_phenotypes'], list):
        obj.model_phenotypes = []
        for item in map['model_phenotypes']:
            obj.model_phenotypes.append(bioentity.Phenotype.fromMap(item))
    if 'human_phenotypes' in map and isinstance(map['human_phenotypes'], list):
        obj.human_phenotypes = []
        for item in map['human_phenotypes']:
            obj.human_phenotypes.append(bioentity.Phenotype.fromMap(item))
    if  'disease_id' in map:
        obj.disease_id = map['disease_id']
    if 'urls' in map and isinstance(map['urls'], list):
        obj.urls = []
        for item in map['urls']:
            obj.urls.append(evidence_linkout.Linkout.fromMap(item))
    if  'evidence_codes' in map:
        obj.evidence_codes = map['evidence_codes']
    for key in map:
      if not key in cls_keys:
        logger.warn("Disease_Model_Association - invalid field - {0} found".format(key))
        return
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Disease_Model_Association
    :returns: number of errors found during validation
    """
    error = 0
    # cumulate errors from super class
    error = error + super(Disease_Model_Association, self).validate(logger, path = path)
    if self.provenance_type is None:
      logger.error("Disease_Model_Association - {0}.provenance_type is required".format(path))
      error = error + 1
    if self.is_associated is None:
      logger.error("Disease_Model_Association - {0}.is_associated is required".format(path))
      error = error + 1
    if self.resource_score is None:
      logger.error("Disease_Model_Association - {0}.resource_score is required".format(path))
      error = error + 1
    if self.date_asserted is None:
      logger.error("Disease_Model_Association - {0}.date_asserted is required".format(path))
      error = error + 1
    # model_id is mandatory
    if self.model_id is None :
        logger.error("Disease_Model_Association - {0}.model_id is required".format(path))
        error = error + 1
    if self.model_id and not isinstance(self.model_id, basestring):
        logger.error("Disease_Model_Association - {0}.model_id type should be a string".format(path))
        error = error + 1
    # model_phenotypes is mandatory
    if self.model_phenotypes is None :
        logger.error("Disease_Model_Association - {0}.model_phenotypes is required".format(path))
        error = error + 1
    if not self.model_phenotypes is None and len(self.model_phenotypes) > 0 and not all(isinstance(n, bioentity.Phenotype) for n in self.model_phenotypes):
        logger.error("Disease_Model_Association - {0}.model_phenotypes array should have elements of type 'bioentity.Phenotype'".format(path))
        error = error+1
    if self.model_phenotypes and len(self.model_phenotypes) < 1:
        logger.error("Disease_Model_Association - {0}.model_phenotypes array should have at least 1 elements".format(path))
        error = error + 1
    # human_phenotypes is mandatory
    if self.human_phenotypes is None :
        logger.error("Disease_Model_Association - {0}.human_phenotypes is required".format(path))
        error = error + 1
    if not self.human_phenotypes is None and len(self.human_phenotypes) > 0 and not all(isinstance(n, bioentity.Phenotype) for n in self.human_phenotypes):
        logger.error("Disease_Model_Association - {0}.human_phenotypes array should have elements of type 'bioentity.Phenotype'".format(path))
        error = error+1
    if self.human_phenotypes and len(self.human_phenotypes) < 1:
        logger.error("Disease_Model_Association - {0}.human_phenotypes array should have at least 1 elements".format(path))
        error = error + 1
    # disease_id is mandatory
    if self.disease_id is None :
        logger.error("Disease_Model_Association - {0}.disease_id is required".format(path))
        error = error + 1
    """ Check regex: ^http://www.orpha.net/ORDO/Orphanet_[0-9]{1,}|http://purl.obolibrary.org/obo/DOID_[0-9]{2,}|http://www.ebi.ac.uk/efo/EFO_[0-9]{4,}|http://purl.obolibrary.org/obo/HP_[0-9]{4,}|http://purl.obolibrary.org/obo/GO_[0-9]{4,}|http://purl.obolibrary.org/obo/MP_[0-9]{3,}$ for validation"""
    if self.disease_id and not re.match('^http://www.orpha.net/ORDO/Orphanet_[0-9]{1,}|http://purl.obolibrary.org/obo/DOID_[0-9]{2,}|http://www.ebi.ac.uk/efo/EFO_[0-9]{4,}|http://purl.obolibrary.org/obo/HP_[0-9]{4,}|http://purl.obolibrary.org/obo/GO_[0-9]{4,}|http://purl.obolibrary.org/obo/MP_[0-9]{3,}$', self.disease_id):
        logger.error("Disease_Model_Association - {0}.disease_id '{1}'".format(path,self.disease_id) + " does not match pattern '^http://www.orpha.net/ORDO/Orphanet_[0-9]{1,}|http://purl.obolibrary.org/obo/DOID_[0-9]{2,}|http://www.ebi.ac.uk/efo/EFO_[0-9]{4,}|http://purl.obolibrary.org/obo/HP_[0-9]{4,}|http://purl.obolibrary.org/obo/GO_[0-9]{4,}|http://purl.obolibrary.org/obo/MP_[0-9]{3,}$'")
        logger.warn(json.dumps(self.disease_id, sort_keys=True, indent=2))
    if self.disease_id and not isinstance(self.disease_id, basestring):
        logger.error("Disease_Model_Association - {0}.disease_id type should be a string".format(path))
        error = error + 1
    if not self.urls is None and len(self.urls) > 0 and not all(isinstance(n, evidence_linkout.Linkout) for n in self.urls):
        logger.error("Disease_Model_Association - {0}.urls array should have elements of type 'evidence_linkout.Linkout'".format(path))
        error = error+1
    # evidence_codes is mandatory
    if self.evidence_codes is None :
        logger.error("Disease_Model_Association - {0}.evidence_codes is required".format(path))
        error = error + 1
    if not self.evidence_codes is None:
        validValues = ['http://identifiers.org/eco/ECO:0000057']
        for item in self.evidence_codes:
            if item not in validValues:
                logger.error("Disease_Model_Association - {0}.evidence_codes value is restricted to the fixed set of values 'http://identifiers.org/eco/ECO:0000057' ('{1}' given)".format(path, item))
                error = error + 1
    if not self.evidence_codes is None and len(self.evidence_codes) > 0 and not all(isinstance(n, basestring) for n in self.evidence_codes):
        logger.error("Disease_Model_Association - {0}.evidence_codes array should have elements of type 'basestring'".format(path))
        error = error+1
    if self.evidence_codes and len(self.evidence_codes) < 1:
        logger.error("Disease_Model_Association - {0}.evidence_codes array should have at least 1 elements".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = super(Disease_Model_Association, self).serialize()
    if not self.model_id is None: classDict['model_id'] = self.model_id
    if not self.model_phenotypes is None: classDict['model_phenotypes'] = map(lambda x: x.serialize(), self.model_phenotypes)
    if not self.human_phenotypes is None: classDict['human_phenotypes'] = map(lambda x: x.serialize(), self.human_phenotypes)
    if not self.disease_id is None: classDict['disease_id'] = self.disease_id
    if not self.urls is None: classDict['urls'] = map(lambda x: x.serialize(), self.urls)
    if not self.evidence_codes is None: classDict['evidence_codes'] = self.evidence_codes
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
