'''
Created on Oct 10, 2017

@author: Dounaa
'''

class JsonPathParser(object):
    '''
    Parses the json messages. Given a specified path to an element, attempts to extract that element from the specified document.
    
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def find_value(self, json_path, json_document):
        path = json_path.split(".")
        
        return self.__process_path(json_document, path, 0, len(path) - 1)

    
    def __process_path(self, json_doc, path, path_index, max_index):
        path_element = path[path_index]
        
        array_index = path_element.find('[]') 
        
        #element in the specified path is an array. Process the first element of it
        if (array_index != -1):             
            elem_name = path_element[:array_index]
            return self.__process_path(json_doc[elem_name][0], path, path_index + 1, max_index)
        #found the last element in the path. return the value
        elif (path_index == max_index):    
            return json_doc[path_element]
        #continue iteration through json doc
        else:                                
            return self.__process_path(json_doc[path_element], path, path_index + 1, max_index)
        
                
            
    
  