# sflogdownloader

Using salesforce api, download all Cases (including correspondence) owned by particular people and parse the output for aws links to download and extract attachments (log files) in to newly created directories.

Script expects presence of file called "credentials.txt" at same level formatted like:

"
example@user
examplePassword
exampleSalesForceAPIKey
"
