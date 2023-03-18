# flake8: noqa
CISCO_BPA_DOCS = """

API Documentation

1.
BASE URL: https://bpa-adhoc4.cisco.com/bpa/api/v1.0/


Get list of all the devices

Gets the list of all the devices under every NSO


API path: device-manager/devices


Parameters
Query parameters
limit 	
String
Number of devices to display per page
page 	
String
Page index
search 	
String
Search By devices
sort 	
String
Sort column by device name
nsoInstance 	
String
NSO Instance of the devices


2
BASE URL: https://bpa-adhoc4.cisco.com/bpa/api/v1.0/

API name : Get Device Details : Gets details of the device given name and its NSO Instance


API path: device-manager/device/{device-name}
Path parameters
device-name 	
String 
Device name to get details   
Required

Query parameters
nsoInstance	
String 
NSO Instance of the device  
Required

Additional optional URL parameters will be added. For API stability, no required parameters will be added in the future!"""