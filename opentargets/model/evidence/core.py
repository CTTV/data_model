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
import opentargets.model.evidence.association_score as evidence_association_score
import opentargets.model.evidence.linkout as evidence_linkout
import opentargets.model.evidence.mutation as evidence_mutation

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
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/base.json
"""
class Base(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param unique_experiment_reference = None
  :param is_associated = False
  :param date_asserted = None
  :param resource_score = None
  :param     provenance_type = None
  """
  def __init__(self, unique_experiment_reference = None, is_associated = False, date_asserted = None, resource_score = None,     provenance_type = None):
    
    """
    Name: unique_experiment_reference
    Type: string
    Description: A unique experiment identifier or literature reference that uniquely identifies the study in your database
    """
    self.unique_experiment_reference = unique_experiment_reference
    
    """
    Name: is_associated
    Type: boolean
    """
    self.is_associated = is_associated
    
    """
    Name: date_asserted
    Type: string
    Description: date the evidence was made public
    String format: date-time
    """
    self.date_asserted = date_asserted
    """
    Name: resource_score
    """
    self.resource_score = resource_score
    """
    Name: provenance_type
    """
    self.provenance_type = provenance_type
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.unique_experiment_reference:
        obj.unique_experiment_reference = clone.unique_experiment_reference
    if clone.is_associated:
        obj.is_associated = clone.is_associated
    if clone.date_asserted:
        obj.date_asserted = clone.date_asserted
    if clone.resource_score:
        obj.resource_score = clone.resource_score
    if clone.provenance_type:
        obj.provenance_type = BaseProvenance_Type.cloneObject(clone.provenance_type)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['unique_experiment_reference','is_associated','date_asserted','resource_score','provenance_type']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("Base - DictType expected - {0} found\n".format(type(map)))
      return
    if  'unique_experiment_reference' in map:
        obj.unique_experiment_reference = map['unique_experiment_reference']
    if  'is_associated' in map:
        obj.is_associated = map['is_associated']
    if  'date_asserted' in map:
        obj.date_asserted = map['date_asserted']
    if 'resource_score' in map:
        if not evidence_association_score.Pvalue.fromMap(map['resource_score']) is None:
            obj.resource_score = evidence_association_score.Pvalue.fromMap(map['resource_score'])
        elif not evidence_association_score.Probability.fromMap(map['resource_score']) is None:
            obj.resource_score = evidence_association_score.Probability.fromMap(map['resource_score'])
        elif not evidence_association_score.Rank.fromMap(map['resource_score']) is None:
            obj.resource_score = evidence_association_score.Rank.fromMap(map['resource_score'])
        elif not evidence_association_score.Summed_Total.fromMap(map['resource_score']) is None:
            obj.resource_score = evidence_association_score.Summed_Total.fromMap(map['resource_score'])
        else:
            raise opentargets.model.core.JSONException("resource_score can't be cast to any class")
    if  'provenance_type' in map:
        obj.provenance_type = BaseProvenance_Type.fromMap(map['provenance_type'])
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Base
    :returns: number of errors found during validation
    """
    error = 0
    """ Check regex: http://europepmc.org/abstract/MED/[0-9]+|http://europepmc.org/articles/PMC[0-9]{4,}|[doi|DOI|https://dx.doi.org/]*[\s\.\:]{0,2}(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'])\S)+)|STUDYID_.+$ for validation"""
    if self.unique_experiment_reference and not re.match('http://europepmc.org/abstract/MED/[0-9]+|http://europepmc.org/articles/PMC[0-9]{4,}|[doi|DOI|https://dx.doi.org/]*[\s\.\:]{0,2}(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'])\S)+)|STUDYID_.+$', self.unique_experiment_reference):
        logger.error("Base - {0}.unique_experiment_reference '{1}'".format(path,self.unique_experiment_reference) + " does not match pattern 'http://europepmc.org/abstract/MED/[0-9]+|http://europepmc.org/articles/PMC[0-9]{4,}|[doi|DOI|https://dx.doi.org/]*[\s\.\:]{0,2}(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'])\S)+)|STUDYID_.+$'")
        logger.warn(json.dumps(self.unique_experiment_reference, sort_keys=True, indent=2))
    if self.unique_experiment_reference and not isinstance(self.unique_experiment_reference, six.string_types):
        logger.error("Base - {0}.unique_experiment_reference type should be a string".format(path))
        error = error + 1
    if self.is_associated and not type(self.is_associated) is bool:
        logger.error("Base - {0}.is_associated type should be a boolean".format(path))
        error = error + 1
    if not self.date_asserted is None:
        try:
            iso8601.parse_date(self.date_asserted)
        except iso8601.ParseError as e:
            logger.error("Base - {0}.date_asserted '{1}' invalid ISO 8601 date (YYYY-MM-DDThh:mm:ss.sTZD expected)".format(path, self.date_asserted))
            error = error+1
    if self.date_asserted and not isinstance(self.date_asserted, six.string_types):
        logger.error("Base - {0}.date_asserted type should be a string".format(path))
        error = error + 1
        if not ( isinstance(self.resource_score, evidence_association_score.Pvalue) or isinstance(self.resource_score, evidence_association_score.Probability) or isinstance(self.resource_score, evidence_association_score.Rank) or isinstance(self.resource_score, evidence_association_score.Summed_Total)):
            logger.error("Base - {0}.resource_score incorrect type".format(path))
            error = error + 1
        else:
            resource_score_error = self.resource_score.validate(logger, path = '.'.join([path, 'resource_score']))
            error = error + resource_score_error
    if self.provenance_type:
        if not isinstance(self.provenance_type, BaseProvenance_Type):
            logger.error("BaseProvenance_Type class instance expected for attribute - {0}.provenance_type".format(path))
            error = error + 1
        else:
            provenance_type_error = self.provenance_type.validate(logger, path = '.'.join([path, 'provenance_type']))
            error = error + provenance_type_error
    return error
  def date_assertedto_isoformat(self):
    iso8601.parse_date(self.date_asserted).isoformat()
  
  def serialize(self):
    classDict = dict()
    if not self.unique_experiment_reference is None: classDict['unique_experiment_reference'] = self.unique_experiment_reference
    if not self.is_associated is None: classDict['is_associated'] = self.is_associated
    if not self.date_asserted is None: classDict['date_asserted'] = self.date_asserted
    if not self.resource_score is None: classDict['resource_score'] = self.resource_score.serialize()
    if not self.provenance_type is None: classDict['provenance_type'] = self.provenance_type.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/base.json/definitions/single_lit_reference
"""
class Single_Lit_Reference(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param lit_id = None
  :param     rank = None
  :param mined_sentences = None
  """
  def __init__(self, lit_id = None,     rank = None, mined_sentences = None):
    
    """
    Name: lit_id
    Type: string
    Description: Note for pubmed identifiers, use the URI http://europepmc.org/abstract/MED/[0-9]+
    Required: {True}
    """
    self.lit_id = lit_id
    """
    Name: rank
    """
    self.rank = rank
    
    """
    Name: mined_sentences
    Type: array
    """
    self.mined_sentences = mined_sentences
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.lit_id:
        obj.lit_id = clone.lit_id
    if clone.rank:
        obj.rank = evidence_association_score.Rank.cloneObject(clone.rank)
    if clone.mined_sentences:
        obj.mined_sentences = []; obj.mined_sentences.extend(clone.mined_sentences)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['lit_id','rank','mined_sentences']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("Single_Lit_Reference - DictType expected - {0} found\n".format(type(map)))
      return
    if  'lit_id' in map:
        obj.lit_id = map['lit_id']
    if  'rank' in map:
        obj.rank = evidence_association_score.Rank.fromMap(map['rank'])
    if 'mined_sentences' in map and isinstance(map['mined_sentences'], list):
        obj.mined_sentences = []
        for item in map['mined_sentences']:
            obj.mined_sentences.append(Base_Mined_Sentences_Item.fromMap(item))
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Single_Lit_Reference
    :returns: number of errors found during validation
    """
    error = 0
    # lit_id is mandatory
    if self.lit_id is None :
        logger.error("Single_Lit_Reference - {0}.lit_id is required".format(path))
        error = error + 1
    """ Check regex: http://europepmc.org/abstract/MED/[0-9]+|http://europepmc.org/articles/PMC[0-9]{4,}|[doi|DOI|https://dx.doi.org/]*[\s\.\:]{0,2}(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'])\S)+)$ for validation"""
    if self.lit_id and not re.match('http://europepmc.org/abstract/MED/[0-9]+|http://europepmc.org/articles/PMC[0-9]{4,}|[doi|DOI|https://dx.doi.org/]*[\s\.\:]{0,2}(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'])\S)+)$', self.lit_id):
        logger.error("Single_Lit_Reference - {0}.lit_id '{1}'".format(path,self.lit_id) + " does not match pattern 'http://europepmc.org/abstract/MED/[0-9]+|http://europepmc.org/articles/PMC[0-9]{4,}|[doi|DOI|https://dx.doi.org/]*[\s\.\:]{0,2}(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'])\S)+)$'")
        logger.warn(json.dumps(self.lit_id, sort_keys=True, indent=2))
    if self.lit_id and not isinstance(self.lit_id, six.string_types):
        logger.error("Single_Lit_Reference - {0}.lit_id type should be a string".format(path))
        error = error + 1
    if self.rank:
        if not isinstance(self.rank, evidence_association_score.Rank):
            logger.error("evidence_association_score.Rank class instance expected for attribute - {0}.rank".format(path))
            error = error + 1
        else:
            rank_error = self.rank.validate(logger, path = '.'.join([path, 'rank']))
            error = error + rank_error
    if not self.mined_sentences is None and len(self.mined_sentences) > 0 and not all(isinstance(n, Base_Mined_Sentences_Item) for n in self.mined_sentences):
        logger.error("Single_Lit_Reference - {0}.mined_sentences array should have elements of type 'Base_Mined_Sentences_Item'".format(path))
        error = error+1
    if self.mined_sentences and len(self.mined_sentences) < 1:
        logger.error("Single_Lit_Reference - {0}.mined_sentences array should have at least 1 elements".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.lit_id is None: classDict['lit_id'] = self.lit_id
    if not self.rank is None: classDict['rank'] = self.rank.serialize()
    if not self.mined_sentences is None: classDict['mined_sentences'] = map(lambda x: x.serialize(), self.mined_sentences)
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/base.json/definitions/single_lit_reference inner class:(_mined_sentences_item)
"""
class Base_Mined_Sentences_Item(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param text = None
  :param section = None
  :param t_start = None
  :param t_end = None
  :param d_start = None
  :param d_end = None
  """
  def __init__(self, text = None, section = None, t_start = None, t_end = None, d_start = None, d_end = None):
    
    """
    Name: text
    Type: string
    Required: {True}
    """
    self.text = text
    
    """
    Name: section
    Type: string
    Description: Section of the article in which this sentence appears
    Required: {True}
    """
    self.section = section
    
    """
    Name: t_start
    Type: number
    Description: Start co-ordinate of target (protein/gene) in text
    """
    self.t_start = t_start
    
    """
    Name: t_end
    Type: number
    Description: End co-ordinate of target (protein/gene) in text
    """
    self.t_end = t_end
    
    """
    Name: d_start
    Type: number
    Description: Start co-ordinate of disease name in text
    """
    self.d_start = d_start
    
    """
    Name: d_end
    Type: number
    Description: End co-ordinate of disease name in text
    """
    self.d_end = d_end
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.text:
        obj.text = clone.text
    if clone.section:
        obj.section = clone.section
    if clone.t_start:
        obj.t_start = clone.t_start
    if clone.t_end:
        obj.t_end = clone.t_end
    if clone.d_start:
        obj.d_start = clone.d_start
    if clone.d_end:
        obj.d_end = clone.d_end
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['text','section','t_start','t_end','d_start','d_end']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("Base_Mined_Sentences_Item - DictType expected - {0} found\n".format(type(map)))
      return
    if  'text' in map:
        obj.text = map['text']
    if  'section' in map:
        obj.section = map['section']
    if  't_start' in map:
        obj.t_start = map['t_start']
    if  't_end' in map:
        obj.t_end = map['t_end']
    if  'd_start' in map:
        obj.d_start = map['d_start']
    if  'd_end' in map:
        obj.d_end = map['d_end']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class Base_Mined_Sentences_Item
    :returns: number of errors found during validation
    """
    error = 0
    # text is mandatory
    if self.text is None :
        logger.error("Base_Mined_Sentences_Item - {0}.text is required".format(path))
        error = error + 1
    if self.text and not isinstance(self.text, six.string_types):
        logger.error("Base_Mined_Sentences_Item - {0}.text type should be a string".format(path))
        error = error + 1
    # section is mandatory
    if self.section is None :
        logger.error("Base_Mined_Sentences_Item - {0}.section is required".format(path))
        error = error + 1
    if not self.section is None and not self.section in ['title','abstract','introduction_and_background','results','discussion','case_study','conclusion_and_future_work','appendix','figure','table','other']:
        logger.error("Base_Mined_Sentences_Item - {0}.section value is restricted to the fixed set of values 'title','abstract','introduction_and_background','results','discussion','case_study','conclusion_and_future_work','appendix','figure','table','other' ('{1}' given)".format(path, self.section))
        error = error + 1
    if self.section and not isinstance(self.section, six.string_types):
        logger.error("Base_Mined_Sentences_Item - {0}.section type should be a string".format(path))
        error = error + 1
    if self.t_start is not None and (self.t_start < 0):
        logger.error("Base_Mined_Sentences_Item - {0}.t_start: {1} should be greater than or equal to 0".format(path, self.t_start))
        error = error+1
    if self.t_end is not None and (self.t_end < 0):
        logger.error("Base_Mined_Sentences_Item - {0}.t_end: {1} should be greater than or equal to 0".format(path, self.t_end))
        error = error+1
    if self.d_start is not None and (self.d_start < 0):
        logger.error("Base_Mined_Sentences_Item - {0}.d_start: {1} should be greater than or equal to 0".format(path, self.d_start))
        error = error+1
    if self.d_end is not None and (self.d_end < 0):
        logger.error("Base_Mined_Sentences_Item - {0}.d_end: {1} should be greater than or equal to 0".format(path, self.d_end))
        error = error+1
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.text is None: classDict['text'] = self.text
    if not self.section is None: classDict['section'] = self.section
    if not self.t_start is None: classDict['t_start'] = self.t_start
    if not self.t_end is None: classDict['t_end'] = self.t_end
    if not self.d_start is None: classDict['d_start'] = self.d_start
    if not self.d_end is None: classDict['d_end'] = self.d_end
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/base.json inner class:(provenance_type)
"""
class BaseProvenance_Type(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param     expert = None
  :param     literature = None
  :param     database = None
  """
  def __init__(self,     expert = None,     literature = None,     database = None):
    """
    Name: expert
    """
    self.expert = expert
    """
    Name: literature
    """
    self.literature = literature
    """
    Name: database
    """
    self.database = database
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.expert:
        obj.expert = BaseExpert.cloneObject(clone.expert)
    if clone.literature:
        obj.literature = BaseLiterature.cloneObject(clone.literature)
    if clone.database:
        obj.database = BaseDatabase.cloneObject(clone.database)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['expert','literature','database']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("BaseProvenance_Type - DictType expected - {0} found\n".format(type(map)))
      return
    if  'expert' in map:
        obj.expert = BaseExpert.fromMap(map['expert'])
    if  'literature' in map:
        obj.literature = BaseLiterature.fromMap(map['literature'])
    if  'database' in map:
        obj.database = BaseDatabase.fromMap(map['database'])
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class BaseProvenance_Type
    :returns: number of errors found during validation
    """
    error = 0
    if self.expert:
        if not isinstance(self.expert, BaseExpert):
            logger.error("BaseExpert class instance expected for attribute - {0}.expert".format(path))
            error = error + 1
        else:
            expert_error = self.expert.validate(logger, path = '.'.join([path, 'expert']))
            error = error + expert_error
    if self.literature:
        if not isinstance(self.literature, BaseLiterature):
            logger.error("BaseLiterature class instance expected for attribute - {0}.literature".format(path))
            error = error + 1
        else:
            literature_error = self.literature.validate(logger, path = '.'.join([path, 'literature']))
            error = error + literature_error
    if self.database:
        if not isinstance(self.database, BaseDatabase):
            logger.error("BaseDatabase class instance expected for attribute - {0}.database".format(path))
            error = error + 1
        else:
            database_error = self.database.validate(logger, path = '.'.join([path, 'database']))
            error = error + database_error
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.expert is None: classDict['expert'] = self.expert.serialize()
    if not self.literature is None: classDict['literature'] = self.literature.serialize()
    if not self.database is None: classDict['database'] = self.database.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/base.json inner class:(expert)
"""
class BaseExpert(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param statement = None
  :param     author = None
  :param status = False
  """
  def __init__(self, statement = None,     author = None, status = False):
    
    """
    Name: statement
    Type: string
    """
    self.statement = statement
    """
    Name: author
    """
    self.author = author
    
    """
    Name: status
    Type: boolean
    Required: {True}
    """
    self.status = status
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.statement:
        obj.statement = clone.statement
    if clone.author:
        obj.author = BaseAuthor.cloneObject(clone.author)
    if clone.status:
        obj.status = clone.status
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['statement','author','status']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("BaseExpert - DictType expected - {0} found\n".format(type(map)))
      return
    if  'statement' in map:
        obj.statement = map['statement']
    if  'author' in map:
        obj.author = BaseAuthor.fromMap(map['author'])
    if  'status' in map:
        obj.status = map['status']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class BaseExpert
    :returns: number of errors found during validation
    """
    error = 0
    if self.statement and not isinstance(self.statement, six.string_types):
        logger.error("BaseExpert - {0}.statement type should be a string".format(path))
        error = error + 1
    if self.author:
        if not isinstance(self.author, BaseAuthor):
            logger.error("BaseAuthor class instance expected for attribute - {0}.author".format(path))
            error = error + 1
        else:
            author_error = self.author.validate(logger, path = '.'.join([path, 'author']))
            error = error + author_error
    # status is mandatory
    if self.status is None :
        logger.error("BaseExpert - {0}.status is required".format(path))
        error = error + 1
    if self.status and not type(self.status) is bool:
        logger.error("BaseExpert - {0}.status type should be a boolean".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.statement is None: classDict['statement'] = self.statement
    if not self.author is None: classDict['author'] = self.author.serialize()
    if not self.status is None: classDict['status'] = self.status
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/base.json inner class:(author)
"""
class BaseAuthor(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param organization = None
  :param email = None
  :param name = None
  """
  def __init__(self, organization = None, email = None, name = None):
    
    """
    Name: organization
    Type: string
    """
    self.organization = organization
    
    """
    Name: email
    Type: string
    String format: email
    """
    self.email = email
    
    """
    Name: name
    Type: string
    """
    self.name = name
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.organization:
        obj.organization = clone.organization
    if clone.email:
        obj.email = clone.email
    if clone.name:
        obj.name = clone.name
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['organization','email','name']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("BaseAuthor - DictType expected - {0} found\n".format(type(map)))
      return
    if  'organization' in map:
        obj.organization = map['organization']
    if  'email' in map:
        obj.email = map['email']
    if  'name' in map:
        obj.name = map['name']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class BaseAuthor
    :returns: number of errors found during validation
    """
    error = 0
    if self.organization and not isinstance(self.organization, six.string_types):
        logger.error("BaseAuthor - {0}.organization type should be a string".format(path))
        error = error + 1
    if not self.email is None and not re.match('[\w.-]+@[\w.-]+.\w+', self.email):
        logger.error("BaseAuthor - {0}.email '{1}' is not a valid email address".format(path, self.email))
        logger.error(self.to_JSON)
        error = error + 1
    if self.email and not isinstance(self.email, six.string_types):
        logger.error("BaseAuthor - {0}.email type should be a string".format(path))
        error = error + 1
    if self.name and not isinstance(self.name, six.string_types):
        logger.error("BaseAuthor - {0}.name type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.organization is None: classDict['organization'] = self.organization
    if not self.email is None: classDict['email'] = self.email
    if not self.name is None: classDict['name'] = self.name
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/base.json inner class:(literature)
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
    Required: {True}
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
            obj.references.append(Single_Lit_Reference.fromMap(item))
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class BaseLiterature
    :returns: number of errors found during validation
    """
    error = 0
    # references is mandatory
    if self.references is None :
        logger.error("BaseLiterature - {0}.references is required".format(path))
        error = error + 1
    if not self.references is None and len(self.references) > 0 and not all(isinstance(n, Single_Lit_Reference) for n in self.references):
        logger.error("BaseLiterature - {0}.references array should have elements of type 'Single_Lit_Reference'".format(path))
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
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/base.json inner class:(database)
"""
class BaseDatabase(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param     dbxref = None
  :param id = None
  :param version = None
  """
  def __init__(self,     dbxref = None, id = None, version = None):
    """
    Name: dbxref
    """
    self.dbxref = dbxref
    
    """
    Name: id
    Type: string
    Required: {True}
    """
    self.id = id
    
    """
    Name: version
    Type: string
    Required: {True}
    """
    self.version = version
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.dbxref:
        obj.dbxref = BaseDbxref.cloneObject(clone.dbxref)
    if clone.id:
        obj.id = clone.id
    if clone.version:
        obj.version = clone.version
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['dbxref','id','version']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("BaseDatabase - DictType expected - {0} found\n".format(type(map)))
      return
    if  'dbxref' in map:
        obj.dbxref = BaseDbxref.fromMap(map['dbxref'])
    if  'id' in map:
        obj.id = map['id']
    if  'version' in map:
        obj.version = map['version']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class BaseDatabase
    :returns: number of errors found during validation
    """
    error = 0
    if self.dbxref:
        if not isinstance(self.dbxref, BaseDbxref):
            logger.error("BaseDbxref class instance expected for attribute - {0}.dbxref".format(path))
            error = error + 1
        else:
            dbxref_error = self.dbxref.validate(logger, path = '.'.join([path, 'dbxref']))
            error = error + dbxref_error
    # id is mandatory
    if self.id is None :
        logger.error("BaseDatabase - {0}.id is required".format(path))
        error = error + 1
    if self.id and not isinstance(self.id, six.string_types):
        logger.error("BaseDatabase - {0}.id type should be a string".format(path))
        error = error + 1
    # version is mandatory
    if self.version is None :
        logger.error("BaseDatabase - {0}.version is required".format(path))
        error = error + 1
    if self.version and not isinstance(self.version, six.string_types):
        logger.error("BaseDatabase - {0}.version type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.dbxref is None: classDict['dbxref'] = self.dbxref.serialize()
    if not self.id is None: classDict['id'] = self.id
    if not self.version is None: classDict['version'] = self.version
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/base.json inner class:(dbxref)
"""
class BaseDbxref(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param id = None
  :param url = None
  :param version = None
  """
  def __init__(self, id = None, url = None, version = None):
    
    """
    Name: id
    Type: string
    Description: Please provide the original DB name
    Required: {True}
    """
    self.id = id
    
    """
    Name: url
    Type: string
    Description: Please provide a pointer to the original resource: e.g. http://identifiers.org/orphanet/93298
    String format: uri
    """
    self.url = url
    
    """
    Name: version
    Type: string
    Required: {True}
    """
    self.version = version
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.id:
        obj.id = clone.id
    if clone.url:
        obj.url = clone.url
    if clone.version:
        obj.version = clone.version
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['id','url','version']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("BaseDbxref - DictType expected - {0} found\n".format(type(map)))
      return
    if  'id' in map:
        obj.id = map['id']
    if  'url' in map:
        obj.url = map['url']
    if  'version' in map:
        obj.version = map['version']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class BaseDbxref
    :returns: number of errors found during validation
    """
    error = 0
    # id is mandatory
    if self.id is None :
        logger.error("BaseDbxref - {0}.id is required".format(path))
        error = error + 1
    if self.id and not isinstance(self.id, six.string_types):
        logger.error("BaseDbxref - {0}.id type should be a string".format(path))
        error = error + 1
    if self.url and not isinstance(self.url, six.string_types):
        logger.error("BaseDbxref - {0}.url type should be a string".format(path))
        error = error + 1
    # version is mandatory
    if self.version is None :
        logger.error("BaseDbxref - {0}.version is required".format(path))
        error = error + 1
    if self.version and not isinstance(self.version, six.string_types):
        logger.error("BaseDbxref - {0}.version type should be a string".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.id is None: classDict['id'] = self.id
    if not self.url is None: classDict['url'] = self.url
    if not self.version is None: classDict['version'] = self.version
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/expression.json
"""
class Expression(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param organism_part = None
  :param comparison_name = None
  :param log2_fold_change = None
  :param test_sample = None
  :param reference_sample = None
  :param test_replicates_n = 0
  :param reference_replicates_n = 0
  :param confidence_level = None
  :param experiment_overview = None
  :param evidence_codes = None
  :param urls = None
  :param unique_experiment_reference = None
  :param is_associated = False
  :param date_asserted = None
  :param resource_score = None
  :param     provenance_type = None
  """
  def __init__(self, organism_part = None, comparison_name = None, log2_fold_change = None, test_sample = None, reference_sample = None, test_replicates_n = 0, reference_replicates_n = 0, confidence_level = None, experiment_overview = None, evidence_codes = None, urls = None, unique_experiment_reference = None, is_associated = False, date_asserted = None, resource_score = None,     provenance_type = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Expression, self).__init__(unique_experiment_reference = unique_experiment_reference,is_associated = is_associated,date_asserted = date_asserted,resource_score = resource_score,provenance_type = provenance_type)
    
    """
    Name: organism_part
    Type: string
    """
    self.organism_part = organism_part
    
    """
    Name: comparison_name
    Type: string
    Required: {True}
    """
    self.comparison_name = comparison_name
    """
    Name: log2_fold_change
    """
    self.log2_fold_change = log2_fold_change
    
    """
    Name: test_sample
    Type: string
    Description: Free text - test sample
    Required: {True}
    """
    self.test_sample = test_sample
    
    """
    Name: reference_sample
    Type: string
    Description: Free text - reference sample
    Required: {True}
    """
    self.reference_sample = reference_sample
    
    """
    Name: test_replicates_n
    Type: number
    Description: Count of test replicates
    Required: {True}
    """
    self.test_replicates_n = test_replicates_n
    
    """
    Name: reference_replicates_n
    Type: number
    Description: Count of reference replicates
    Required: {True}
    """
    self.reference_replicates_n = reference_replicates_n
    
    """
    Name: confidence_level
    Type: string
    Description: high = if the disease state is the only variable (i.e. case vs control); medium = if the disease is a variable but there is one or more other variables; low = where all samples have the disease but the variable is something else e.g. a treatment
    Required: {True}
    """
    self.confidence_level = confidence_level
    
    """
    Name: experiment_overview
    Type: string
    Required: {True}
    """
    self.experiment_overview = experiment_overview
    
    """
    Name: evidence_codes
    Type: array
    Description: An array of evidence codes
    Required: {True}
    """
    self.evidence_codes = evidence_codes
    
    """
    Name: urls
    Type: array
    """
    self.urls = urls
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Expression, cls).cloneObject(clone)
    if clone.organism_part:
        obj.organism_part = clone.organism_part
    if clone.comparison_name:
        obj.comparison_name = clone.comparison_name
    obj.log2_fold_change = ExpressionLog2_Fold_Change.cloneObject(clone.log2_fold_change)
    if clone.test_sample:
        obj.test_sample = clone.test_sample
    if clone.reference_sample:
        obj.reference_sample = clone.reference_sample
    if clone.test_replicates_n:
        obj.test_replicates_n = clone.test_replicates_n
    if clone.reference_replicates_n:
        obj.reference_replicates_n = clone.reference_replicates_n
    if clone.confidence_level:
        obj.confidence_level = clone.confidence_level
    if clone.experiment_overview:
        obj.experiment_overview = clone.experiment_overview
    if clone.evidence_codes:
        obj.evidence_codes = []; obj.evidence_codes.extend(clone.evidence_codes)
    if clone.urls:
        obj.urls = []; obj.urls.extend(clone.urls)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['organism_part','comparison_name','log2_fold_change','test_sample','reference_sample','test_replicates_n','reference_replicates_n','confidence_level','experiment_overview','evidence_codes','urls','unique_experiment_reference','is_associated','date_asserted','resource_score','provenance_type']
    obj = super(Expression, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Expression - DictType expected - {0} found\n".format(type(map)))
      return
    if  'organism_part' in map:
        obj.organism_part = map['organism_part']
    if  'comparison_name' in map:
        obj.comparison_name = map['comparison_name']
    if  'log2_fold_change' in map:
        obj.log2_fold_change = ExpressionLog2_Fold_Change.fromMap(map['log2_fold_change'])
    if  'test_sample' in map:
        obj.test_sample = map['test_sample']
    if  'reference_sample' in map:
        obj.reference_sample = map['reference_sample']
    if  'test_replicates_n' in map:
        obj.test_replicates_n = map['test_replicates_n']
    if  'reference_replicates_n' in map:
        obj.reference_replicates_n = map['reference_replicates_n']
    if  'confidence_level' in map:
        obj.confidence_level = map['confidence_level']
    if  'experiment_overview' in map:
        obj.experiment_overview = map['experiment_overview']
    if  'evidence_codes' in map:
        obj.evidence_codes = map['evidence_codes']
    if 'urls' in map and isinstance(map['urls'], list):
        obj.urls = []
        for item in map['urls']:
            obj.urls.append(evidence_linkout.Linkout.fromMap(item))
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
    if self.unique_experiment_reference is None:
      logger.error("Expression - {0}.unique_experiment_reference is required".format(path))
      error = error + 1
    if self.is_associated is None:
      logger.error("Expression - {0}.is_associated is required".format(path))
      error = error + 1
    if self.date_asserted is None:
      logger.error("Expression - {0}.date_asserted is required".format(path))
      error = error + 1
    if self.resource_score is None:
      logger.error("Expression - {0}.resource_score is required".format(path))
      error = error + 1
    if self.provenance_type is None:
      logger.error("Expression - {0}.provenance_type is required".format(path))
      error = error + 1
    if self.organism_part and not isinstance(self.organism_part, six.string_types):
        logger.error("Expression - {0}.organism_part type should be a string".format(path))
        error = error + 1
    # comparison_name is mandatory
    if self.comparison_name is None :
        logger.error("Expression - {0}.comparison_name is required".format(path))
        error = error + 1
    if self.comparison_name and not isinstance(self.comparison_name, six.string_types):
        logger.error("Expression - {0}.comparison_name type should be a string".format(path))
        error = error + 1
    if self.log2_fold_change is None:
        logger.error("Expression - {0}.log2_fold_change is required".format(path))
        error = error + 1
    elif not isinstance(self.log2_fold_change, ExpressionLog2_Fold_Change):
        logger.error("ExpressionLog2_Fold_Change class instance expected for attribute - {0}.log2_fold_change".format(path))
        error = error + 1
    else:
        log2_fold_change_error = self.log2_fold_change.validate(logger, path = '.'.join([path, 'log2_fold_change']))
        error = error + log2_fold_change_error
    # test_sample is mandatory
    if self.test_sample is None :
        logger.error("Expression - {0}.test_sample is required".format(path))
        error = error + 1
    if self.test_sample and not isinstance(self.test_sample, six.string_types):
        logger.error("Expression - {0}.test_sample type should be a string".format(path))
        error = error + 1
    # reference_sample is mandatory
    if self.reference_sample is None :
        logger.error("Expression - {0}.reference_sample is required".format(path))
        error = error + 1
    if self.reference_sample and not isinstance(self.reference_sample, six.string_types):
        logger.error("Expression - {0}.reference_sample type should be a string".format(path))
        error = error + 1
    # test_replicates_n is mandatory
    if self.test_replicates_n is None :
        logger.error("Expression - {0}.test_replicates_n is required".format(path))
        error = error + 1
    if self.test_replicates_n < 1:
        logger.error("Expression - {0}.test_replicates_n: {1} should be greater than or equal to 1".format(path, self.test_replicates_n))
        error = error+1
    # reference_replicates_n is mandatory
    if self.reference_replicates_n is None :
        logger.error("Expression - {0}.reference_replicates_n is required".format(path))
        error = error + 1
    if self.reference_replicates_n < 1:
        logger.error("Expression - {0}.reference_replicates_n: {1} should be greater than or equal to 1".format(path, self.reference_replicates_n))
        error = error+1
    # confidence_level is mandatory
    if self.confidence_level is None :
        logger.error("Expression - {0}.confidence_level is required".format(path))
        error = error + 1
    if not self.confidence_level is None and not self.confidence_level in ['high','medium','low']:
        logger.error("Expression - {0}.confidence_level value is restricted to the fixed set of values 'high','medium','low' ('{1}' given)".format(path, self.confidence_level))
        error = error + 1
    if self.confidence_level and not isinstance(self.confidence_level, six.string_types):
        logger.error("Expression - {0}.confidence_level type should be a string".format(path))
        error = error + 1
    # experiment_overview is mandatory
    if self.experiment_overview is None :
        logger.error("Expression - {0}.experiment_overview is required".format(path))
        error = error + 1
    if self.experiment_overview and not isinstance(self.experiment_overview, six.string_types):
        logger.error("Expression - {0}.experiment_overview type should be a string".format(path))
        error = error + 1
    # evidence_codes is mandatory
    if self.evidence_codes is None :
        logger.error("Expression - {0}.evidence_codes is required".format(path))
        error = error + 1
    if not self.evidence_codes is None:
        validValues = ['http://purl.obolibrary.org/obo/ECO_0000356','http://purl.obolibrary.org/obo/ECO_0000357','http://purl.obolibrary.org/obo/ECO_0000358','http://purl.obolibrary.org/obo/ECO_0000359','http://purl.obolibrary.org/obo/ECO_0000205']
        for item in self.evidence_codes:
            if item not in validValues:
                logger.error("Expression - {0}.evidence_codes value is restricted to the fixed set of values 'http://purl.obolibrary.org/obo/ECO_0000356','http://purl.obolibrary.org/obo/ECO_0000357','http://purl.obolibrary.org/obo/ECO_0000358','http://purl.obolibrary.org/obo/ECO_0000359','http://purl.obolibrary.org/obo/ECO_0000205' ('{1}' given)".format(path, item))
                error = error + 1
    if not self.evidence_codes is None and len(self.evidence_codes) > 0 and not all(isinstance(n, six.string_types) for n in self.evidence_codes):
        logger.error("Expression - {0}.evidence_codes array should have elements of type 'six.string_types'".format(path))
        error = error+1
    if self.evidence_codes and len(self.evidence_codes) < 1:
        logger.error("Expression - {0}.evidence_codes array should have at least 1 elements".format(path))
        error = error + 1
    if not self.urls is None and len(self.urls) > 0 and not all(isinstance(n, evidence_linkout.Linkout) for n in self.urls):
        logger.error("Expression - {0}.urls array should have elements of type 'evidence_linkout.Linkout'".format(path))
        error = error+1
    return error
  
  def serialize(self):
    classDict = super(Expression, self).serialize()
    if not self.organism_part is None: classDict['organism_part'] = self.organism_part
    if not self.comparison_name is None: classDict['comparison_name'] = self.comparison_name
    if not self.log2_fold_change is None: classDict['log2_fold_change'] = self.log2_fold_change.serialize()
    if not self.test_sample is None: classDict['test_sample'] = self.test_sample
    if not self.reference_sample is None: classDict['reference_sample'] = self.reference_sample
    if not self.test_replicates_n is None: classDict['test_replicates_n'] = self.test_replicates_n
    if not self.reference_replicates_n is None: classDict['reference_replicates_n'] = self.reference_replicates_n
    if not self.confidence_level is None: classDict['confidence_level'] = self.confidence_level
    if not self.experiment_overview is None: classDict['experiment_overview'] = self.experiment_overview
    if not self.evidence_codes is None: classDict['evidence_codes'] = self.evidence_codes
    if not self.urls is None: classDict['urls'] = map(lambda x: x.serialize(), self.urls)
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/expression.json inner class:(log2_fold_change)
"""
class ExpressionLog2_Fold_Change(object):
  """
  Constructor using all fields with default values
  Arguments:
  :param value = 0
  :param percentile_rank = 0
  """
  def __init__(self, value = 0, percentile_rank = 0):
    
    """
    Name: value
    Type: number
    Required: {True}
    """
    self.value = value
    
    """
    Name: percentile_rank
    Type: number
    Required: {True}
    """
    self.percentile_rank = percentile_rank
  
  @classmethod
  def cloneObject(cls, clone):
    obj = cls()
    if clone.value:
        obj.value = clone.value
    if clone.percentile_rank:
        obj.percentile_rank = clone.percentile_rank
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['value','percentile_rank']
    obj = cls()
    if not isinstance(map, types.DictType):
      logger.warn("ExpressionLog2_Fold_Change - DictType expected - {0} found\n".format(type(map)))
      return
    if  'value' in map:
        obj.value = map['value']
    if  'percentile_rank' in map:
        obj.percentile_rank = map['percentile_rank']
    return obj
  
  def validate(self, logger, path = "root"):
    """
    Validate class ExpressionLog2_Fold_Change
    :returns: number of errors found during validation
    """
    error = 0
    # value is mandatory
    if self.value is None :
        logger.error("ExpressionLog2_Fold_Change - {0}.value is required".format(path))
        error = error + 1
    # percentile_rank is mandatory
    if self.percentile_rank is None :
        logger.error("ExpressionLog2_Fold_Change - {0}.percentile_rank is required".format(path))
        error = error + 1
    return error
  
  def serialize(self):
    classDict = dict()
    if not self.value is None: classDict['value'] = self.value
    if not self.percentile_rank is None: classDict['percentile_rank'] = self.percentile_rank
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/literature_curated.json
"""
class Literature_Curated(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param clinical_significance = None
  :param evidence_codes = None
  :param known_mutations = None
  :param urls = None
  :param unique_experiment_reference = None
  :param is_associated = False
  :param date_asserted = None
  :param resource_score = None
  :param     provenance_type = None
  """
  def __init__(self, clinical_significance = None, evidence_codes = None, known_mutations = None, urls = None, unique_experiment_reference = None, is_associated = False, date_asserted = None, resource_score = None,     provenance_type = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Literature_Curated, self).__init__(unique_experiment_reference = unique_experiment_reference,is_associated = is_associated,date_asserted = date_asserted,resource_score = resource_score,provenance_type = provenance_type)
    
    """
    Name: clinical_significance
    Type: string
    """
    self.clinical_significance = clinical_significance
    
    """
    Name: evidence_codes
    Type: array
    Description: An array of evidence codes
    Required: {True}
    """
    self.evidence_codes = evidence_codes
    
    """
    Name: known_mutations
    Type: array
    Description: An array of mutations
    """
    self.known_mutations = known_mutations
    
    """
    Name: urls
    Type: array
    """
    self.urls = urls
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Literature_Curated, cls).cloneObject(clone)
    if clone.clinical_significance:
        obj.clinical_significance = clone.clinical_significance
    if clone.evidence_codes:
        obj.evidence_codes = []; obj.evidence_codes.extend(clone.evidence_codes)
    if clone.known_mutations:
        obj.known_mutations = []; obj.known_mutations.extend(clone.known_mutations)
    if clone.urls:
        obj.urls = []; obj.urls.extend(clone.urls)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['clinical_significance','evidence_codes','known_mutations','urls','unique_experiment_reference','is_associated','date_asserted','resource_score','provenance_type']
    obj = super(Literature_Curated, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Literature_Curated - DictType expected - {0} found\n".format(type(map)))
      return
    if  'clinical_significance' in map:
        obj.clinical_significance = map['clinical_significance']
    if  'evidence_codes' in map:
        obj.evidence_codes = map['evidence_codes']
    if 'known_mutations' in map and isinstance(map['known_mutations'], list):
        obj.known_mutations = []
        for item in map['known_mutations']:
            obj.known_mutations.append(evidence_mutation.Mutation.fromMap(item))
    if 'urls' in map and isinstance(map['urls'], list):
        obj.urls = []
        for item in map['urls']:
            obj.urls.append(evidence_linkout.Linkout.fromMap(item))
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
    if self.is_associated is None:
      logger.error("Literature_Curated - {0}.is_associated is required".format(path))
      error = error + 1
    if self.date_asserted is None:
      logger.error("Literature_Curated - {0}.date_asserted is required".format(path))
      error = error + 1
    if self.resource_score is None:
      logger.error("Literature_Curated - {0}.resource_score is required".format(path))
      error = error + 1
    if self.provenance_type is None:
      logger.error("Literature_Curated - {0}.provenance_type is required".format(path))
      error = error + 1
    if not self.clinical_significance is None and not self.clinical_significance in ['Pathogenic','Likely pathogenic','protective','association','risk_factor','Affects','drug response']:
        logger.error("Literature_Curated - {0}.clinical_significance value is restricted to the fixed set of values 'Pathogenic','Likely pathogenic','protective','association','risk_factor','Affects','drug response' ('{1}' given)".format(path, self.clinical_significance))
        error = error + 1
    if self.clinical_significance and not isinstance(self.clinical_significance, six.string_types):
        logger.error("Literature_Curated - {0}.clinical_significance type should be a string".format(path))
        error = error + 1
    # evidence_codes is mandatory
    if self.evidence_codes is None :
        logger.error("Literature_Curated - {0}.evidence_codes is required".format(path))
        error = error + 1
    if not self.evidence_codes is None:
        validValues = ['http://purl.obolibrary.org/obo/ECO_0000213','http://purl.obolibrary.org/obo/ECO_0000305','http://www.targetvalidation.org/evidence/literature_mining','http://purl.obolibrary.org/obo/ECO_0000204','http://purl.obolibrary.org/obo/ECO_0000205','http://purl.obolibrary.org/obo/ECO_0000053']
        for item in self.evidence_codes:
            if item not in validValues:
                logger.error("Literature_Curated - {0}.evidence_codes value is restricted to the fixed set of values 'http://purl.obolibrary.org/obo/ECO_0000213','http://purl.obolibrary.org/obo/ECO_0000305','http://www.targetvalidation.org/evidence/literature_mining','http://purl.obolibrary.org/obo/ECO_0000204','http://purl.obolibrary.org/obo/ECO_0000205','http://purl.obolibrary.org/obo/ECO_0000053' ('{1}' given)".format(path, item))
                error = error + 1
    if not self.evidence_codes is None and len(self.evidence_codes) > 0 and not all(isinstance(n, six.string_types) for n in self.evidence_codes):
        logger.error("Literature_Curated - {0}.evidence_codes array should have elements of type 'six.string_types'".format(path))
        error = error+1
    if self.evidence_codes and len(self.evidence_codes) < 1:
        logger.error("Literature_Curated - {0}.evidence_codes array should have at least 1 elements".format(path))
        error = error + 1
    if not self.known_mutations is None and len(self.known_mutations) > 0 and not all(isinstance(n, evidence_mutation.Mutation) for n in self.known_mutations):
        logger.error("Literature_Curated - {0}.known_mutations array should have elements of type 'evidence_mutation.Mutation'".format(path))
        error = error+1
    if self.known_mutations and len(self.known_mutations) < 0:
        logger.error("Literature_Curated - {0}.known_mutations array should have at least 0 elements".format(path))
        error = error + 1
    if not self.urls is None and len(self.urls) > 0 and not all(isinstance(n, evidence_linkout.Linkout) for n in self.urls):
        logger.error("Literature_Curated - {0}.urls array should have elements of type 'evidence_linkout.Linkout'".format(path))
        error = error+1
    return error
  
  def serialize(self):
    classDict = super(Literature_Curated, self).serialize()
    if not self.clinical_significance is None: classDict['clinical_significance'] = self.clinical_significance
    if not self.evidence_codes is None: classDict['evidence_codes'] = self.evidence_codes
    if not self.known_mutations is None: classDict['known_mutations'] = map(lambda x: x.serialize(), self.known_mutations)
    if not self.urls is None: classDict['urls'] = map(lambda x: x.serialize(), self.urls)
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)

"""
https://raw.githubusercontent.com/opentargets/json_schema/master/src/evidence/literature_mining.json
"""
class Literature_Mining(Base):
  """
  Constructor using all fields with default values
  Arguments:
  :param evidence_codes = None
  :param literature_ref = None
  :param unique_experiment_reference = None
  :param is_associated = False
  :param date_asserted = None
  :param resource_score = None
  :param     provenance_type = None
  """
  def __init__(self, evidence_codes = None, literature_ref = None, unique_experiment_reference = None, is_associated = False, date_asserted = None, resource_score = None,     provenance_type = None):
    """
    Call super constructor
    BaseClassName.__init__(self, args)
    """
    super(Literature_Mining, self).__init__(unique_experiment_reference = unique_experiment_reference,is_associated = is_associated,date_asserted = date_asserted,resource_score = resource_score,provenance_type = provenance_type)
    
    """
    Name: evidence_codes
    Type: array
    Description: An array of evidence codes
    Required: {True}
    """
    self.evidence_codes = evidence_codes
    """
    Name: literature_ref
    """
    self.literature_ref = literature_ref
  
  @classmethod
  def cloneObject(cls, clone):
    # super will return an instance of the subtype
    obj = super(Literature_Mining, cls).cloneObject(clone)
    if clone.evidence_codes:
        obj.evidence_codes = []; obj.evidence_codes.extend(clone.evidence_codes)
    obj.literature_ref = Single_Lit_Reference.cloneObject(clone.literature_ref)
    return obj
  
  @classmethod
  def fromMap(cls, map):
    cls_keys = ['evidence_codes','literature_ref','unique_experiment_reference','is_associated','date_asserted','resource_score','provenance_type']
    obj = super(Literature_Mining, cls).fromMap(map)
    if not isinstance(map, types.DictType):
      logger.warn("Literature_Mining - DictType expected - {0} found\n".format(type(map)))
      return
    if  'evidence_codes' in map:
        obj.evidence_codes = map['evidence_codes']
    if  'literature_ref' in map:
        obj.literature_ref = Single_Lit_Reference.fromMap(map['literature_ref'])
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
    if self.unique_experiment_reference is None:
      logger.error("Literature_Mining - {0}.unique_experiment_reference is required".format(path))
      error = error + 1
    if self.is_associated is None:
      logger.error("Literature_Mining - {0}.is_associated is required".format(path))
      error = error + 1
    if self.date_asserted is None:
      logger.error("Literature_Mining - {0}.date_asserted is required".format(path))
      error = error + 1
    if self.resource_score is None:
      logger.error("Literature_Mining - {0}.resource_score is required".format(path))
      error = error + 1
    if self.provenance_type is None:
      logger.error("Literature_Mining - {0}.provenance_type is required".format(path))
      error = error + 1
    # evidence_codes is mandatory
    if self.evidence_codes is None :
        logger.error("Literature_Mining - {0}.evidence_codes is required".format(path))
        error = error + 1
    if not self.evidence_codes is None:
        validValues = ['http://www.targetvalidation.org/evidence/literature_mining','http://purl.obolibrary.org/obo/ECO_0000213']
        for item in self.evidence_codes:
            if item not in validValues:
                logger.error("Literature_Mining - {0}.evidence_codes value is restricted to the fixed set of values 'http://www.targetvalidation.org/evidence/literature_mining','http://purl.obolibrary.org/obo/ECO_0000213' ('{1}' given)".format(path, item))
                error = error + 1
    if not self.evidence_codes is None and len(self.evidence_codes) > 0 and not all(isinstance(n, six.string_types) for n in self.evidence_codes):
        logger.error("Literature_Mining - {0}.evidence_codes array should have elements of type 'six.string_types'".format(path))
        error = error+1
    if self.evidence_codes and len(self.evidence_codes) < 1:
        logger.error("Literature_Mining - {0}.evidence_codes array should have at least 1 elements".format(path))
        error = error + 1
    if self.literature_ref is None:
        logger.error("Literature_Mining - {0}.literature_ref is required".format(path))
        error = error + 1
    elif not isinstance(self.literature_ref, Single_Lit_Reference):
        logger.error("Single_Lit_Reference class instance expected for attribute - {0}.literature_ref".format(path))
        error = error + 1
    else:
        literature_ref_error = self.literature_ref.validate(logger, path = '.'.join([path, 'literature_ref']))
        error = error + literature_ref_error
    return error
  
  def serialize(self):
    classDict = super(Literature_Mining, self).serialize()
    if not self.evidence_codes is None: classDict['evidence_codes'] = self.evidence_codes
    if not self.literature_ref is None: classDict['literature_ref'] = self.literature_ref.serialize()
    return classDict
  
  def to_JSON(self, indentation=4):
    return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)
