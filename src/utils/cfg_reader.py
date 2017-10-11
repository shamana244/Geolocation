'''
Created on Oct 10, 2017

This module contains classes required for reading of the config files and command line inputs.


SafeConfigParserBuilder:
 - builds a SafeConfigParser. This is used for dependency injection to make testing easier
 
ConfigLoader: 
 - reads and loads ini files for local and 3rd party configuration 
 - uses SafeConfigParserBuilder

CommandLineReader:
 - Responsible for reading and parsing command line input. If the input is not valid, 
   or not all of the input criteria are met, the program exists.
 
@author: Dounaa
'''

import argparse
import logging
import sys
from configparser import SafeConfigParser

class ConfigLoader(object):
    '''
    Responsible for loading configuration files and storing the properties that were loaded.
    If the load is successful:
     - local_svc_props property will contain properties loaded for local service
     - third_pty_props property will contain properties for the 3rd party geolocation providers
    '''
   
    # Read-only field accessors   
   
    # contains local webservice configuration properties
    @property
    def local_svc_props(self):
        return self._local_props
    

    # contains 3rd party geolocation configuration properties
    @property
    def third_pty_props(self):
        return self._remote_props
    

    # Constructor
    # prop_file_loader - responsible for reading properties. Should be of type properties.PropertyFileLoader
    # config_parser_builder - builds ConfigParser. should be of type SafeConfigParserBuilder
    def __init__(self, prop_file_loader, config_parser_builder):
        self._prop_file_loader = prop_file_loader
        self._config_parser_builder = config_parser_builder
        
    # Load the configuration files provided
    # local_svc_cfg_file - local config file
    # third_pty_cfg_file - 3rd party geolocation provider config file
    def load_configs(self, local_svc_cfg_file, third_pty_cfg_file):
        
        self._local_props = self._prop_file_loader.read_properties(local_svc_cfg_file, self._config_parser_builder.build())
        logging.debug(self._local_props)
        
        self._remote_props = self._prop_file_loader.read_properties(third_pty_cfg_file, self._config_parser_builder.build())
        logging.debug(self._remote_props)
        
        logging.info("Configs successfully loaded")

class SafeConfigParserBuilder(object):
    '''
    Just constructs SafeConfigParser. This class exists only to help with testing via DI
    '''
    
    def build(self):
        return SafeConfigParser()


class CommandLineReader(object):
    '''
    CommandLineReader is responsible for reading and parsing command line input.
    If the input is not valid, or not all of the input criteria are met, the program exists.
    '''
       
    # full path to the webservice configuration file
    @property
    def local_svc_cfg_file(self):
        return self._local_svc_cfg_file
    
    # full path to the 3rd party geolocation configuration file
    @property
    def third_pty_cfg_file(self):
        return self._third_pty_cfg_file
    
    # reads command line arguments and sets properties if successful
    # exists the application if encounters errors
    def read_command_line(self, argv):
        try:      
            parser = argparse.ArgumentParser()
            parser.add_argument("-l", type=str, help="ini file containing this service properties (host, port, etc)")
            parser.add_argument("-t", type=str, help="ini file containing 3rd party geolocation provider properties")
            
            args = parser.parse_args()
            
            if(args.l and args.t):
                self._third_pty_cfg_file = args.t
                self._local_svc_cfg_file = args.l
            
        except:        
            logging.error("Error occured. Please run with -h to see usage.")             
            sys.exit(2)