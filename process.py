from download import ftp
from download import s3
import os
import getcases

def createDir(caseNumber, LogDestBase):
    if not os.path.exists("{}/{}".format(LogDestBase, caseNumber)):
        os.makedirs("{}/{}".format(LogDestBase, caseNumber))

def getCasesContent(sf, LogDestBase, sfOwnerId):
    records = getcases.getSalesforceCases(LogDestBase, sfOwnerId)
    print "Destination: {}".format(LogDestBase)
    for i in range(0, len(records)):
        caseNumber = records[i]['CaseNumber']

        ftpLogLocation = records[i]['LogLocationFTPURL__c']
        caseDetailResult = sf.query("SELECT Status,ToAddress,TextBody, \
                                    CreatedDate,FromAddress,FromName, \
                                    HasAttachment,Headers,Id,Incoming, \
                                    IsDeleted,LastModifiedById, \
                                    LastModifiedDate,MessageDate,ParentId, \
                                    ReplyToEmailMessageId,Subject, \
                                    SystemModstamp FROM EmailMessage where \
                                    ParentId in (SELECT Id FROM Case where \
                                    Case_External_ID__c = '{}')".format \
                                    (records[i]['Case_External_ID__c']))
        caseDetailResult = caseDetailResult['records']

        print "Processing", caseNumber
        # check if FTP exists:
        if ftpLogLocation is not None and len(ftpLogLocation) < 60:
            ftp.downloadFTP(caseNumber, ftpLogLocation, LogDestBase)

        # check if AWS S3 files exist:
        for i in caseDetailResult:
            text = i.items()[3][1]
            if text is None:
                pass
                # fail silently
            else:
                if "amazonaws" in text:
                    createDir(caseNumber, LogDestBase)
                    s3.downloadS3(text, caseNumber, LogDestBase)
                else:
                    ###    print "OVER 220: ", text.encode('cp1252')
                    splitting = text.split("\n\n")
                    for listItem in splitting:
                        if "amazonaws" in listItem:
                            s3.downloadS3(text, caseNumber, LogDestBase)
