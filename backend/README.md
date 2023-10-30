# Introduction
Datasheet tool backend to handle datasheets between frontend and database system
# API Endpoints
Brief description of Backend endpoints
## /backup-datasheets
### Method GET
### Parameters
None
### Return Value
Path to backup file
## /download-backup/<path:filename>
### Method GET
### Parameters
None
### Return Value
Backup JSON file
## /backup-files
### Method GET
### Parameters
None
### Return Value
List of backup file paths
## /datasheets-numberic-to-human-readable
### Method GET
### Parameters
None
### Return Value
List of datasheets in human readable form
## /datasheets-delete/<int:id>
### Method DELETE
### Parameters
- id : Id of the datasheet to be deleted
### Return Value
None
## /datasheets-search
### Method POST
### Parameters
- selectedCheckboxes : array critical issues in the for such as "module_properties.performance.issue_1"
- filter : String containing the free text search parameter
### Return Value
array of datasheet dictionaries 
## /datasheets
Return all datasheets that are (or are not) validated against market place
### Method GET
### Parameters
- validate: Int value 1 or 0 to select if datasheets need to be validated or not
### Return Value
array of datasheet dictionaries
## /datasheets
Create new datasheet
### Method POST
### Parameters
- data: JSON data including Keycloak Id of the user and Datasheet
### Return Value
None
## /datasheets
### Method PUT
Update existing datasheets
### Parameters
- data: JSON data including id of the datasheet to be updated
### Return Value
None
## /datasheets
### Method GET
### Parameters
- id : Id of the datasheet to be deleted
### Return Value
None