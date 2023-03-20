# flake8: noqa
CISCO_BPA_DOCS = """

API Documentation

1.
BASE URL: https://bpa-adhoc4.cisco.com/bpa/api/v1.0/


Get list of all the devices

Gets the list of all the devices under every NSO


API path: device-manager/devices 
method: GET


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
method:GET
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

3.
BASE URL: https://bpa-adhoc4.cisco.com/bpa/api/v1.0/

Get list of controllers under each device


Gets list of all the controllers under a device given its name


API path:device-manager/device/{device-name}/controllers
method:GET
Path parameters
device-name 	
String 
Device name to get details   
Required

4. Edit the device details

Edits the given device by name, under the NSO specified


API path:/api/v1.0/device-manager/devices?nsoInstance=&action=edit
method:PUT

Query paramters:
1.nsoInstance required
string
required

2.action    required
string
required

Body parameters:
[
{
name:
string

address:
string

admin-state:
string

authgroup:
string

description:
string

device-type:
string

latitude:
string

longitude:
string

ned-id:
string
port:
integer
protocol:
string
}
]
"""