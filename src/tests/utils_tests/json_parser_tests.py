'''
Created on Oct 11, 2017

@author: Dounaa
'''
import unittest
import json
from utils.json_parser import JsonPathParser, JsonParsingException

class JsonPathParserTest(unittest.TestCase):

    #"{ \"results\": { \"geometry\": {\"location\": [{\"key\": \"value\"},{\"some_other_key\": \"some other value\"}]}}}"
        
    def setUp(self):
        self._parser = JsonPathParser()
        
        
    def tearDown(self):
        del self._parser


    def test_find_value_simple_path(self):
        #setup
        expected_value = "some message"
        json_msg = json.loads(json.dumps({'results': {'key': expected_value }}))
        path = "results.key";
        
        #run & assert
        self._run_and_assert(path, json_msg, expected_value)
    
    def test_find_value_array_start_of_path(self):
        #setup
        expected_value = "some message"
        json_msg = json.loads(json.dumps({'header':[{'results': {'key': expected_value }}]}))
        path = "header[].results.key";
        
        #run & assert
        self._run_and_assert(path, json_msg, expected_value)
    
    def test_find_value_array_middle_of_path(self):
        #setup
        expected_value = "some message"
        json_msg = json.loads(json.dumps({'header':[{'results': [{'key': expected_value, 'otherKey' : 'othervalue'}]}]}))
        path = "header[].results[].key";
        
        #run & assert
        self._run_and_assert(path, json_msg, expected_value)
    
    def test_find_value_throws_exception(self):
        #setup
        expected_value = "some message"
        json_msg = json.loads(json.dumps({'results': {'key': expected_value }}))
        path = "results.bar";
        
        #run & assert
        self.assertRaises(JsonParsingException, self._parser.find_value, path, json_msg)
    
    def test_find_value_throws_exception_not_json_object(self):
        #setup
        json_msg = "some string value"
        path = "results.bar";
        
        #run & assert
        self.assertRaises(JsonParsingException, self._parser.find_value, path, json_msg)
        
    def _run_and_assert(self, path, json_msg, expected_value):
        #run test
        value = self._parser.find_value(path, json_msg)
        
        #assert
        assert(value == expected_value)
        
class JsonParsingExceptionTest(unittest.TestCase):
    
    def test_message(self):
        #setup
        message = "Test message"
        
        #run test
        ex = JsonParsingException(message)
        
        #assert
        assert(str(ex) == message)

if __name__ == "__main__":
    unittest.main()