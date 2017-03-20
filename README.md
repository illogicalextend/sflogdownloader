# sflogdownloader

Using Salesforce API, examine all Cases (including correspondence) owned by particular people and parse the output for Amazon S3 and FTP links to download and extract attachments (log files) in to newly created directories.

To run:

Clone repository.

Populate `credentials.txt` with your Salesforce Username, Password and Security Token.

Modify `sflogdownloader.py` to include your desired log destination under "LogDestBase" and your Salesforce Owner ID under "sfOwnerId".

Run `pip install -r requirements.txt` (also make sure "unzip" server utility is installed)

Run `python downloader.py`
