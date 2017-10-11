'''
Created on Oct 9, 2017

@author: Dounaa
'''

class PropertyFileLoader(object):
    '''
    Loads property file for the service
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
            
    def read_properties(self, file_path, configParser):
        '''
        Returns properties that are read from file
        '''        
        configParser.optionxform = str
        configParser.read(file_path)
        results = {}
        
        for section in configParser.sections():
            results[section] = self.__load_config_section(section, configParser)

        return results
    
    def __load_config_section(self, section, configParser):
        '''
        attempts to load the specified section in the config file
        '''
        dictionary = {}
        
        options = configParser.options(section)

        for option in options:
            dictionary[option] = configParser.get(section, option)
            if dictionary[option] == -1:
                raise ValueError("%s is not found in section %s" % (option, section) )
        
        return dictionary