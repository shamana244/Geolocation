'''
Created on Oct 10, 2017

@author: Dounaa
'''
import argparse
import sys
from configparser import SafeConfigParser

class CommandLineReader(object):
    '''
    classdocs
    '''
    @property
    def local_svc_props(self):
        return self.__local_props
    
    @property
    def third_pty_props(self):
        return self.__remote_props

    def __init__(self, prop_file_loader):
        '''
        Constructor
        '''
        self.__prop_file_loader = prop_file_loader

    def load_configs(self, local_props, remote_props):
        
        self.__local_props = self.__prop_file_loader.read_properties(local_props, SafeConfigParser())
        print (self.__local_props)
        
        self.__remote_props = self.__prop_file_loader.read_properties(remote_props, SafeConfigParser())
        print (self.__remote_props)
    
    def read_command_line(self, argv):
        try:      
            parser = argparse.ArgumentParser()
            parser.add_argument("-l", type=str, help="ini file containing this service properties (host, port, etc)")
            parser.add_argument("-t", type=str, help="ini file containing 3rd party geolocation provider properties")
            
            args = parser.parse_args()
            
            if(args.l and args.t):
                self.load_configs(args.l, args.t)
            
        except:        
            print("Error occured. Please run with -h to see usage.")             
            sys.exit(2)