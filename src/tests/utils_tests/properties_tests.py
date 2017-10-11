'''
Created on Oct 11, 2017

@author: Dounaa
'''
import unittest

from configparser import ConfigParser
from unittest.mock import MagicMock
from utils.properties import PropertyFileLoader

class PropertyFileLoaderTest(unittest.TestCase):


    def setUp(self):
        self.pfl = PropertyFileLoader()


    def tearDown(self):
        del self.pfl


    def test_read_properties(self):
        #setup
        sections = {"section1" : {"key1" : "value1", "key2" : "value2"}, "section2" : {"key1" : "value1", "key2" : "value2"}}
        expected_results = {"section1" : {}, "section2" : {}}
        path = "dummy path"
        
        parser = ConfigParser()
        parser.read = MagicMock()
        parser.sections = MagicMock(return_value = sections)
        parser.items = MagicMock()
        
        #run test
        results = self.pfl.read_properties(path, parser)
        
        #assert
        parser.read.assert_called_with(path)
        parser.sections.assert_called()
        assert(results == expected_results)
        
if __name__ == "__main__":
    unittest.main()