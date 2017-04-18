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

__author__ = "Gautier Koscielny"
__copyright__ = "Copyright 2014-2017, Open Targets"
__credits__ = ["Gautier Koscielny", "Samiul Hasan"]
__license__ = "Apache 2.0"
__version__ = "1.2.5"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautierk@targetvalidation.org"
__status__ = "Production"

logger = logging.getLogger(__name__)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/mutation/mutation.json
"""
class Mutation(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param number_samples_with_mutation_type = None
  :param number_mutated_samples = None
  :param inheritance_pattern = None
  :param functional_consequence = None
  :param preferred_name = None
  :param alternative_names = None
  """
  def __init__(self, number_samples_with_mutation_type = None, number_mutated_samples = None, inheritance_pattern = None, functional_consequence = None, preferred_name = None, alternative_names = None):
    
    """
    Name: number_samples_with_mutation_type
    Type: number
    Description: The number of samples for this mutation type if known
    """
    self.number_samples_with_mutation_type = number_samples_with_mutation_type
    
    """
    Name: number_mutated_samples
    Type: number
    Description: The total number of samples with any type of mutation if known
    """
    self.number_mutated_samples = number_mutated_samples
    
    """
    Name: inheritance_pattern
    Type: string
    Description: dominant (a single copy of the abnormal allele is sufficient to give rise to the disease), semi-dominant, or recessive (requiring both copies of the gene to have an abnormal allele)
    """
    self.inheritance_pattern = inheritance_pattern
    
    """
    Name: functional_consequence
    Type: string
    Description: For COSMIC: sequence alteration, deletion, missense_variant, stop_gained, terminator_codon_variant, translational product variant, amino acid insertion, conservative decrease in CDS length, mutation causing uncharacterised change of translational product
    Required: {True}
    """
    self.functional_consequence = functional_consequence
    
    """
    Name: preferred_name
    Type: string
    Description: The preferred name for this mutation, e.g. NM_005228.3(EGFR):c.2500G>T (p.Val834Leu)
    Required: {True}
    """
    self.preferred_name = preferred_name
    
    """
    Name: alternative_names
    Type: array
    Description: A list of alternative names for this mutation, if known e.g. NC_000007.14:g.55191749G>T
    """
    self.alternative_names = alternative_names
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.number_samples_with_mutation_type:
        obj.number_samples_with_mutation_type = clone.number_samples_with_mutation_type
    if clone.number_mutated_samples:
        obj.number_mutated_samples = clone.number_mutated_samples
    if clone.inheritance_pattern:
        obj.inheritance_pattern = clone.inheritance_pattern
    if clone.functional_consequence:
        obj.functional_consequence = clone.functional_consequence
    if clone.preferred_name:
        obj.preferred_name = clone.preferred_name
    if clone.alternative_names:
        obj.alternative_names = []; obj.alternative_names.extend(clone.alternative_names)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['number_samples_with_mutation_type','number_mutated_samples','inheritance_pattern','functional_consequence','preferred_name','alternative_names']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("Mutation - DictType expected - {0} found\n".format(type(map)))
      return
    if  'number_samples_with_mutation_type' in map:
        obj.number_samples_with_mutation_type = map['number_samples_with_mutation_type']
    if  'number_mutated_samples' in map:
        obj.number_mutated_samples = map['number_mutated_samples']
    if  'inheritance_pattern' in map:
        obj.inheritance_pattern = map['inheritance_pattern']
    if  'functional_consequence' in map:
        obj.functional_consequence = map['functional_consequence']
    if  'preferred_name' in map:
        obj.preferred_name = map['preferred_name']
    if  'alternative_names' in map:
        obj.alternative_names = map['alternative_names']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Mutation
    :returns: number of errors found during validation
    """
    error = 0
    if self.number_samples_with_mutation_type is not None and (self.number_samples_with_mutation_type < 0):
        logger.error("Mutation - {0}.number_samples_with_mutation_type: {1} should be greater than or equal to 0".format(path, self.number_samples_with_mutation_type))
        error = error+1
    if self.number_mutated_samples is not None and (self.number_mutated_samples < 0):
        logger.error("Mutation - {0}.number_mutated_samples: {1} should be greater than or equal to 0".format(path, self.number_mutated_samples))
        error = error+1
    if not self.inheritance_pattern is None and not self.inheritance_pattern in ['unknown','dominant','semi-dominant','co-dominant','recessive','dominant/recessive','X-linked recessive']:
        logger.error("Mutation - {0}.inheritance_pattern value is restricted to the fixed set of values 'unknown','dominant','semi-dominant','co-dominant','recessive','dominant/recessive','X-linked recessive' ('{1}' given)".format(path, self.inheritance_pattern))
        error = error + 1
    if self.inheritance_pattern and not isinstance(self.inheritance_pattern, basestring):
        logger.error("Mutation - {0}.inheritance_pattern type should be a string".format(path))
        error = error + 1
    # functional_consequence is mandatory
    if self.functional_consequence is None :
        logger.error("Mutation - {0}.functional_consequence is required".format(path))
        error = error + 1
    if not self.functional_consequence is None and not self.functional_consequence in ['http://purl.obolibrary.org/obo/SO_0000159','http://purl.obolibrary.org/obo/SO_0001583','http://purl.obolibrary.org/obo/SO_0001587','http://purl.obolibrary.org/obo/SO_0001590','http://purl.obolibrary.org/obo/SO_1000065','http://purl.obolibrary.org/obo/SO_0001539','http://purl.obolibrary.org/obo/SO_0001605','http://purl.obolibrary.org/obo/SO_0001825','http://purl.obolibrary.org/obo/SO_0001553','http://purl.obolibrary.org/obo/SO_0001059','http://purl.obolibrary.org/obo/SO_0001821','http://purl.obolibrary.org/obo/SO_0001578','http://purl.obolibrary.org/obo/SO_0001630','http://purl.obolibrary.org/obo/SO_0001575','http://purl.obolibrary.org/obo/SO_0001589','http://targetvalidation.org/sequence/nearest_gene_five_prime_end','http://purl.obolibrary.org/obo/SO_0001574','http://purl.obolibrary.org/obo/SO_0001819','http://purl.obolibrary.org/obo/SO_0001822','http://purl.obolibrary.org/obo/SO_0001818','http://purl.obolibrary.org/obo/SO_0001564','http://purl.obolibrary.org/obo/SO_0001565','http://purl.obolibrary.org/obo/SO_0002012','http://purl.obolibrary.org/obo/SO_0001627','http://purl.obolibrary.org/obo/SO_0001060','http://purl.obolibrary.org/obo/SO_0001624']:
        logger.error("Mutation - {0}.functional_consequence value is restricted to the fixed set of values 'http://purl.obolibrary.org/obo/SO_0000159','http://purl.obolibrary.org/obo/SO_0001583','http://purl.obolibrary.org/obo/SO_0001587','http://purl.obolibrary.org/obo/SO_0001590','http://purl.obolibrary.org/obo/SO_1000065','http://purl.obolibrary.org/obo/SO_0001539','http://purl.obolibrary.org/obo/SO_0001605','http://purl.obolibrary.org/obo/SO_0001825','http://purl.obolibrary.org/obo/SO_0001553','http://purl.obolibrary.org/obo/SO_0001059','http://purl.obolibrary.org/obo/SO_0001821','http://purl.obolibrary.org/obo/SO_0001578','http://purl.obolibrary.org/obo/SO_0001630','http://purl.obolibrary.org/obo/SO_0001575','http://purl.obolibrary.org/obo/SO_0001589','http://targetvalidation.org/sequence/nearest_gene_five_prime_end','http://purl.obolibrary.org/obo/SO_0001574','http://purl.obolibrary.org/obo/SO_0001819','http://purl.obolibrary.org/obo/SO_0001822','http://purl.obolibrary.org/obo/SO_0001818','http://purl.obolibrary.org/obo/SO_0001564','http://purl.obolibrary.org/obo/SO_0001565','http://purl.obolibrary.org/obo/SO_0002012','http://purl.obolibrary.org/obo/SO_0001627','http://purl.obolibrary.org/obo/SO_0001060','http://purl.obolibrary.org/obo/SO_0001624' ('{1}' given)".format(path, self.functional_consequence))
        error = error + 1
    if self.functional_consequence and not isinstance(self.functional_consequence, basestring):
        logger.error("Mutation - {0}.functional_consequence type should be a string".format(path))
        error = error + 1
    # preferred_name is mandatory
    if self.preferred_name is None :
        logger.error("Mutation - {0}.preferred_name is required".format(path))
        error = error + 1
    if self.preferred_name and not isinstance(self.preferred_name, basestring):
        logger.error("Mutation - {0}.preferred_name type should be a string".format(path))
        error = error + 1
    if not self.alternative_names is None and len(self.alternative_names) > 0 and not all(isinstance(n, basestring) for n in self.alternative_names):
        logger.error("Mutation - {0}.alternative_names array should have elements of type 'basestring'".format(path))
        error = error+1
    if self.alternative_names and len(self.alternative_names) < 1:
        logger.error("Mutation - {0}.alternative_names array should have at least 1 elements".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = {}
    if not self.number_samples_with_mutation_type is None: classDict['number_samples_with_mutation_type'] = self.number_samples_with_mutation_type
    if not self.number_mutated_samples is None: classDict['number_mutated_samples'] = self.number_mutated_samples
    if not self.inheritance_pattern is None: classDict['inheritance_pattern'] = self.inheritance_pattern
    if not self.functional_consequence is None: classDict['functional_consequence'] = self.functional_consequence
    if not self.preferred_name is None: classDict['preferred_name'] = self.preferred_name
    if not self.alternative_names is None: classDict['alternative_names'] = self.alternative_names
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
