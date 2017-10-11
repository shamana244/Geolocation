####################################################################################
################################### Geolocation ####################################
####################################################################################
 
 
************************************************************************************
************************************* Hot to run ***********************************
************************************************************************************
 To start the service please run: 
   websvc\app.py -t ..\config\3rd_party_svc.ini -l ..\config\local_svc.ini
 
 Unless you changed the configs, the service would be running on http://127.0.0.1:5003
 (See Configuration files below if you need to change host/port)
 
 You will be asked for a username and password. It's defined in local_svc.ini. See
 details below. Currently it's set to:
	- username: foo
	- password: bar
	
 Sample queries:
 http://127.0.0.1:5003/api/geocode/v1.0/json?address=6+Constitution+Ave+NW,+Washington,+DC
 http://127.0.0.1:5003/api/geocode/v1.0/json?address=Champ+de+Mars,+5+Avenue+Anatole+France,+75007+Paris,+France
 http://127.0.0.1:5003/api/geocode/v1.0/json?address=New+York+City
 
 This project was developed and tested using Eclipse (Oxygen) under Windows 10. 
 Chrome and Microsoft Edge used as browsers. 
 
 Since I am not sure what OS or IDE you will be using I cannot tell you exactly 
 how to execute it.
 
************************************************************************************
******************************* Configuration files ********************************
************************************************************************************

In order to run this service, 2 ini files are required:

 - local_svc.ini - contains cofig properties for this service. 
                  
	This currently includes:
	  - HOST - host of the service( currently set to 127.0.0.1 )
	  - PORT - port on which it will listen ( currently set to 5003 )
	  - USERNAME - see comments under REST section for details
	  - PASSWORD - see comments under REST section for details
				  
	HOST and PORT were intentionally put in a file instead of command line. 
	One can imagine multiple different files depending on environment 
	(DEV, QA, PROD) having different hosts and ports. In addition, what is 
	more important, the PROD configuration should reside in a repository 
	(CVS, SVN, GIT, etc) and not be changeable by hand without oversight.
                      
 - 3rd_party_svc.ini - contains definition of all the Geolocation
	services to be used by this webservice. 
        
	There is no limit to the number of 3rd party services used. 
	No service is hardcoded. Each service must have required set of config 
	properties and the resulting Json messages are dynamically parsed.        
	This enables addition/removal of 3rd party services without 
	making any codechanges, just a config change.
         
	The order of the service definition in the ini file is the 
	order of execution of those services - the fallback. To change
	the order of execution, just change the order of the service 
	specification in the ini file.
        
	If the 3rd party svc call succeeds in converting the adddress,
	the results of this service call will be returned in Json format
	with the lat/lon as well as the name of the 3rd party service that 
	provided the data. It does not contain information why (if any) 
	of previous service calls did not return the data. I figured the
	user of this service would not want to be exposed to internal failures.
	If no service/data is available, an error message is returned.
         
	For exact field description and additional information, see 
	comments in the 3rd_party_svc.ini file.
		
	Note: I purpusfully removed my Google key and kept Google as the top service.
	You will see the request fail and move onto the next one. If you want for
	Google to work, just add your own key.

************************************************************************************   
*************************************** REST ***************************************
************************************************************************************   

REST webservice calls that are supported are defined in this file.

Only GET is currently supported since we are only converting address to lat/lon. 
POST, PUT, DELETE, PATCH calls are not supported and return code 405.
See each call for more details.

Since the spec explicitely said that the service should use JSON for data
serialization, I did not set/check the HTTP Accept Header and always
returned Json.

A simple authentication layer was added to the GET call. In real world,
authentication would use a real auth service, however for the purposes of
this exercise, the USERNAME and PASSWORD are stored in the local_svc_props.ini file 
401 error is returned when authentication fails. 

************************************************************************************   
*************************************** URI ****************************************
************************************************************************************  

URI Structure:  /TYPE_OF_CALL/API_TYPE/VERSION/MSG_FORMAT
   
Example: /api/geocode/v1.0/json
   
/api                   - specifies that this is an api call
/api/geocode           - allows the uri to support multiple different apis in the future, 
                         not just geocode
/api/geocode/v1.0      - allows multiple versions to run in parallel. For example for 
                         backwards compatibility. Please see Notes below.
/api/geocode/v1.0/json - specifies the format of expected input/output. This was in 
					     place of looking at HTTP Accept Header as mentioned above.
						 If for example, XML format would later be supported, on 
						 the last part of URI would need to change.

Notes: 
 - Fully RESTful apis honor discovery. However for the purposes of this project
   this seemed to me as a mute point. So if discovery is off the table, versioning 
   is the next best accepted practice. It is obviously easy to remove the version
   from the URI if needed.

 - At this point URI is hardcoded below, however proper versioning and multiple
   format support is possible given the URI structure. 

************************************************************************************
*********************************** Logging ****************************************
************************************************************************************

Logger: currently the configuration is hardcoded in this file. In real life, I would 
to have multiple log files (one per environment: DEV, QA, PROD) that would be read and 
loaded. I did not do this for this project as I deemed it to be out of scope.

************************************************************************************
*********************************** Testing ****************************************
************************************************************************************

Ali told me not to spend more than 1 hour on writing tests, so I don't have full test 
coverage. I don't know what is the accepted way of test package structure in Python 
soI chose one that I've seen work well for Java and C#. 


 
Side note: this is my first Python project. I have attempted to make it as "Pythony" 
as possible, however if something seems Java'eske, C#'y or simply not the Python way, 
please accept my apologies. 

