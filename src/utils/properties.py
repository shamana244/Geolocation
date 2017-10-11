'''
Created on Oct 9, 2017

PropertyFileLoader is responsible for loading properties.
Given a file path to an .ini file and a config parser, 
PropertyFileLoader reads the file and loads the properties 
into a dict. 

@author: Dounaa
'''

class PropertyFileLoader(object):
    
    '''
    Loads a property file.
     - file_path: path to the properties (ini) file to load
     - configParser: configParser to be used for loading. It is
                     passed in every time in because one may want
                     to separate configurations. It is not created
                     inside the function for testing purposes.
    '''        
    def read_properties(self, file_path, configParser):
        '''
        Returns properties that are read from file
        '''        
        configParser.optionxform = str
        configParser.read(file_path)
        results = {}
        
        for section in configParser.sections():
            results[section] = {}
            for option, value in configParser.items(section):
                results[section][option] = value
            
        return results
    