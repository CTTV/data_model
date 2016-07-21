'''
Copyright 2014-2016 EMBL - European Bioinformatics Institute, Wellcome
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
import sys
from pprint import pprint
import json
from collections import OrderedDict
import hashlib
import logging

__author__ = "Michael Maguire"
__copyright__ = "Copyright 2014-2016, Open Targets"
__credits__ = ["Michael Maguire", "Gautier Koscielny", "Samiul Hasan"]
__license__ = "Apache 2.0"
__version__ = "1.2"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautierk@targetvalidation.org"
__status__ = "Production"

logger = logging.getLogger(__name__)

class DatatStructureFlattener:
    '''
    Class to flatten nested Python data structures into ordered dictionaries and to
    compute hexadigests of them when serialised as JSON.
    Used to compute hexadigests for JSON represented as Python data structures so that sub-structure
    order and white space are irrelvant.
    '''
    def __init__(self, data_structure):
        self.data_structure= data_structure
    def flatten(self, structure, key="", path="", flattened=None):
        '''
        Given any Python data structure nested to an arbitrary level, flatten it into an
        ordered dictionary. This method can be improved and simplified.
        Returns a Python dictionary where the levels of nesting are represented by
        successive arrows ("->").
        '''
        if flattened is None:
            flattened = {}
        if type(structure) not in(dict, list):
            flattened[((path + "->") if path else "") + key] = structure
        elif isinstance(structure, list):
            structure.sort()
            for i, item in enumerate(structure):
                self.flatten(item, "%d" % i, path + "->" + key, flattened)
        else:
            for new_key, value in structure.items():
                self.flatten(value, new_key, path + "->" + key, flattened)
        return flattened
    def get_ordered_dict(self):
        '''
        Return an ordered dictionary by processing the standard Python dictionary
        produced by method "flatten()".
        '''
        unordered_dict = self.flatten(self.data_structure)
        ordered_dict = OrderedDict()
        sorted_keys = sorted(unordered_dict.keys())
        for key in sorted_keys:
            key_cleaned = key.strip().replace('->->', '')
            ordered_dict[key_cleaned] = unordered_dict[key]
        return ordered_dict
    def get_hexdigest(self):
        '''
        Return the hexadigest value for a JSON-serialised version of the
        ordered dictionary returned by method "get_ordered_dict()".
        '''
        ordered_dict = self.get_ordered_dict()
        return hashlib.md5(json.dumps(ordered_dict)).hexdigest()
class CompareJsons:
    '''
    Compare two Python data structures and report any differences between them.
    Used to compare Python data structures created from JSON serializations. White space
    and element order are ignored.
    This class takes two Python data structures and uses them to create two instances
    of "DatatStructureFlattener". It uses this class's methods to flatten the data structures
    and generate ordered dictionaries for each of them that are then tested for key differences
    using set operations.
    '''
    def __init__(self, data_structure1, data_structure2):
        self.data_structure1 = data_structure1
        self.data_structure2 = data_structure2
        self.data_structure_flatten1 = DatatStructureFlattener(self.data_structure1)
        self.data_structure_flatten2 = DatatStructureFlattener(self.data_structure2)
        self.data_structure1_od = self.data_structure_flatten1.get_ordered_dict()
        self.data_structure2_od = self.data_structure_flatten2.get_ordered_dict()
    def do_data_structures_differ(self):
        '''
        Check if the hexadigests for the flattened ordered dictionary representation of the two
        data structures are the same. If this method returns True, skip other checks.
        '''
        return self.data_structure_flatten1.get_hexdigest() == self.data_structure_flatten2.get_hexdigest()
    def get_key_change_summary_list(self):
        '''
        Report all key differences between the two ordered dictionaries as a list.
        '''
        keys_set1 = set(self.data_structure1_od.keys())
        keys_set2 = set(self.data_structure2_od.keys())
        key_change_set = keys_set1 ^ keys_set2
        change_summary = []
        for element in key_change_set:
            try:
                data_structure1_od[element]
                change_summary.append('%s is missing in data structure 2.' % (element,))
            except KeyError:
                change_summary.append('%s is missing in data structure 1.' % (element,))
        return change_summary
    def get_value_change_summary_list(self):
        '''
        Report all value differences between the two ordered dictionaries as a list.
        '''
        change_summary = []
        for key in self.data_structure1_od.keys():
            if self.data_structure1_od[key] != self.data_structure2_od[key]:
                change_summary.append(key)
        return change_summary

if __name__ == '__main__':    
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    json_obj1 = json.loads(open(filename1, 'r').read())
    json_obj2 = json.loads(open(filename2, 'r').read())
    json_flat1 = DatatStructureFlattener(json_obj1)
    json_flat2 = DatatStructureFlattener(json_obj2)
    #pprint(json_flat1.get_ordered_dict())
    #pprint(json_flat2.get_ordered_dict())
    
    cmp_json = CompareJsons(json_obj1, json_obj2)
    if not cmp_json.do_data_structures_differ():
        logging.info("They differ")
        logging.info('\n'.join(cmp_json.get_key_change_summary_list()))
        logging.info('\n'.join(cmp_json.get_value_change_summary_list()))
    else:
        logging.info("They do not differ")

