'''
Created on Oct 10, 2017

Given a Json document and a path in a specific format (described below),
attempts to retrive the value from the document by following the path.

path format: 
 - period (.) delimited set of keys to the last key that has the 
   desired value
 - if the value of a key is an array, [] are expected at the end of the key 
 
   NOTE: currently only the first element in the array is analyzed. If 
   requirements change, this would be easy to modify.
   
**********************************EXAMPLE********************************
    let's imagine we have the following Json document
    {
        "results": {
            "geometry": {
                "location": [
                    {
                        "somekey": "value"
                    },
                    {
                        "some_other_key": "some other value"
                    }
                ]
             }
          }
    }
   
   In order to specify the path to get "value", the path would be: 
    - results.geometry.location[].somekey
   
   As mentioned before, only the first element in the array will be processed.
   So current limitation is that there is no way to access "some other value".
   This was intentionally not implemented because there was currently no need.
    
    
@author: Dounaa
'''

class JsonPathParser(object):
    

    '''
    searches the json_document given the json_path and returns the value that was found.
    If the document does not contain the path, JsonParsingException is thrown.
    '''
    def find_value(self, json_path, json_document):
        path = json_path.split(".")
        
        return self._process_path(json_document, path, 0, len(path) - 1)

    '''
    recursive search for through the json document until value is found or exception is thrown
    '''
    def _process_path(self, json_doc, path, path_index, max_index):
        path_element = path[path_index]
              
        #element in the specified path is an array. Process the first element of it
        try:
            #check if key has value of an array
            array_index = path_element.find('[]') 
            
            #if array, continue searching down the first element of the 
            if (array_index != -1):             
                elem_name = path_element[:array_index]
                return self._process_path(json_doc[elem_name][0], path, path_index + 1, max_index)
            
            #found the desired element in the path - return the value
            elif (path_index == max_index):    
                return json_doc[path_element]

            #continue iteration through json doc
            else:                                
                return self._process_path(json_doc[path_element], path, path_index + 1, max_index)
        #exception caught means that the path specified is not in the json document. Raise error            
        except:  
            raise JsonParsingException("Unable to find %s in document" %path_element)

'''
Class that simply wraps Exception to signify that json document could not be parsed.
'''
class JsonParsingException(Exception):
    pass


            
    
  