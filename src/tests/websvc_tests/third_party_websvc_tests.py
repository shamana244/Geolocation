'''
Created on Oct 11, 2017

@author: Dounaa
'''
import unittest
import logging

from utils.constants import ID_STRING, SERVICE_URL, SEARCH_TAG, SERVICE_NAME
from websvc.third_party_websvc import GeoLocService
from unittest.mock import MagicMock
from unittest import mock


'''
this is a mock response object that will be used for requests.get call
depending on passed parameters, it will return different results
'''
def requests_get_mock(*args, **kwargs):
    
    class MockResponse:
    
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0].startswith("url1"):
        return MockResponse({"key1": "value1"}, 200)
    elif args[0].startswith("url2"):
        return MockResponse({"key2": "value2"}, 200)
    elif args[0].startswith("url3"):
        raise Exception("Some error happened")
    
    return MockResponse(None, 404)

class GeoLocServiceTest(unittest.TestCase):

    _id_string = "some id"
    _service_name = "some service"
    _search_tag = "what is the meaning of life?"
    
    
    def setUp(self):
        self._properties = {ID_STRING : self._id_string, 
                            SERVICE_NAME: self._service_name,
                            SEARCH_TAG : self._search_tag}
        self._service = GeoLocService(self._properties)


    def tearDown(self):
        del self._service
        del self._properties

        
    @mock.patch("requests.get", side_effect=requests_get_mock)
    def test_call_service_confirm_url(self, mock_get):
        # setup
        url = "some url"
        self._properties.update({SERVICE_URL : url})         
        address = "123 foo lane, bar city, great country, world"
    
        # run & assert
        self._run_assert_call_service_results(mock_get, url, address, None)
    
          
    @mock.patch("requests.get", side_effect=requests_get_mock)
    def test_call_service_results_url1(self, mock_get):
        # setup
        url = "url1"
        self._properties.update({SERVICE_URL : url})
        
        # run & assert
        self._run_assert_call_service_results(mock_get, url, "some address", {"key1": "value1"})
        
        
    @mock.patch("requests.get", side_effect=requests_get_mock)
    def test_call_service_results_url2(self, mock_get):
        # setup
        url = "url2"
        self._properties.update({SERVICE_URL : url})
        
        # run & assert
        self._run_assert_call_service_results(mock_get, url, "some address", {"key2": "value2"})
    
          
    @mock.patch("requests.get", side_effect=requests_get_mock)
    def test_call_service_exception_caught(self, mock_get):
        # setup
        url = "url3"
        self._properties.update({SERVICE_URL : url})
        logging.warning = MagicMock()
        
        
        # run & assert
        # given url3 is specified, I expect the mock to throw and exception and for it
        # to get caught within the code 
        self._run_assert_call_service_results(mock_get, url, "some address", None)
        
    # helper method that takes in a mock, url and expected result and runs the service      
    def _run_assert_call_service_results(self, mock_get, url, address, expected_result):
        expected_url = url + "?" + self._id_string + "&" + self._search_tag + address
        
        #run test
        result = self._service.call_service(address)
        
        #assert url called is correct & no results returned
        self.assertIn(mock.call(expected_url), mock_get.call_args_list)
        assert(result == expected_result)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()