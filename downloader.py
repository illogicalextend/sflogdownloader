#!/usr/bin/env python

from simple_salesforce import Salesforce
from urlparse import urlparse
from urlparse import urlsplit
import time
import argparse
import sys
import os
import urllib
import humanize

LogDestBase = "/vagrant/project/flaskapp/logs1"

if not os.path.exists(LogDestBase):
    os.makedirs(LogDestBase)

with open('credentials.txt') as f:
    lines = f.read().splitlines()
    sfUsername = lines[0]
    sfPassword = lines[1]
    sfToken = lines[2]

    sf = Salesforce(username='%s' % sfUsername, password='%s' % sfPassword, security_token='%s' % sfToken)
    def downloadLogs():
        print "Destination: {}".format(LogDestBase)
        print "Checking for available logs.."
        #caseListResult = "SELECT CaseNumber, Status, Case_External_ID__c, LogLocationFTPURL__c FROM Case where (Status != 'closed' and Status != 'Closed No Response' and Status != 'Merged' and Status != 'Junk' and Status != 'Closed by Customer' and Status != 'Closed In KB' and Status != 'Call No-Answer') and (OwnerId = '00532000004yymVAAQ' or OwnerId = '00532000003hdv9AAA' or OwnerId = '00532000003i25wAAA' or OwnerId = '00532000004ytb3AAA' or OwnerId = '00532000004yymaAAA' or OwnerId = '00532000004z91pAAA' or OwnerId = '00532000004zGNxAAM' or OwnerId = '00532000004zXpjAAE' or OwnerId = '00532000004zcz0AAA' or OwnerId = '00532000004zkB3AAI' or OwnerId = '00532000005NPnsAAG' or OwnerId = '00532000005UlUNAA0' or OwnerId = '00532000005UlUSAA0' or OwnerId = '00532000005UlUXAA0' or OwnerId = '00532000005V37vAAC' or OwnerId = '005600000029jF0AAI' or OwnerId = '00560000002AsvZAAS' or OwnerId = '00560000003X9XRAA0' or OwnerId = '00560000003XehPAAS') ORDER BY CaseNumber ASC"
        caseListResult = "SELECT CaseNumber, Status, Case_External_ID__c, LogLocationFTPURL__c FROM Case where (Status != 'closed' and Status != 'Closed No Response' and Status != 'Merged' and Status != 'Junk' and Status != 'Closed by Customer' and Status != 'Closed In KB' and Status != 'Call No-Answer') and (OwnerId = '00532000004yymVAAQ') ORDER BY CaseNumber ASC"
        query = sf.query(caseListResult)
        records = query['records']
        for i in range(0, len(records)):
            caseNumber = records[i]['CaseNumber']

            ftpLogLocation = records[i]['LogLocationFTPURL__c']
            caseDetailResult = sf.query("SELECT Status,ToAddress,TextBody,CreatedDate,FromAddress,FromName,HasAttachment,Headers,Id,Incoming,IsDeleted,LastModifiedById,LastModifiedDate,MessageDate,ParentId,ReplyToEmailMessageId,Subject,SystemModstamp FROM EmailMessage where ParentId in (SELECT Id FROM Case where Case_External_ID__c = '{}')".format(records[i]['Case_External_ID__c']))
            caseDetailResult = caseDetailResult['records']

            if ftpLogLocation is not None and len(ftpLogLocation) < 60:
                downloadFTP(caseNumber, ftpLogLocation)
            print "Processing", caseNumber
            for i in caseDetailResult:
                text = i.items()[3][1]
                if text is None:
                    pass
                    # fail silently
                else:
                    if "amazonaws" in text:
                        createDir(caseNumber)
                        processLogs(text, caseNumber)
                    else:
                        ###    print "OVER 220: ", text.encode('cp1252')
                        splitting = text.split("\n\n")
                        for listItem in splitting:
                            if "amazonaws" in listItem:
                                processLogs(text, caseNumber)

def createDir(caseNumber):
    if not os.path.exists("{}/{}".format(LogDestBase, caseNumber)):
        os.makedirs("{}/{}".format(LogDestBase, caseNumber))

# if "amazonaws" is in the salesforce comment
def processLogs(text, caseNumber):
    downloadURL = text[24:]
    if "\n\n" not in text[24:] and len(text[24:]) < 220:
        firstfilename = text[24:].split('/')[-1].split('#')[0].split('?')[0]
        if not os.path.exists("{}/{}/{}/{}".format(LogDestBase, caseNumber, firstfilename[:-4], firstfilename)):
            try:
                if firstfilename[-4:] == ".zip":
                    # create directory (if it doesn't exist) to store contents of zip, by trimming ".zip" and naming directory after filename
                    if not os.path.exists("{}/{}/{}".format(LogDestBase, caseNumber, firstfilename[:-4])):
                        os.makedirs("{}/{}/{}".format(LogDestBase, caseNumber, firstfilename[:-4]))
                    # download full .zip file path to newly created directory
                    printDLSize(downloadURL)
                    urllib.urlretrieve(text[24:], os.path.join("{}/{}/{}".format(LogDestBase, caseNumber, firstfilename[:-4]), firstfilename))
                    os.system("unzip -o -q {}/{}/{}/{} -d {}/{}/{}".format(LogDestBase, caseNumber, firstfilename[:-4], firstfilename, LogDestBase, caseNumber, firstfilename[:-4]))
                else:
                    # else if not .zip, download other type of file and don't try to extract it.
                    if not os.path.exists("{}/{}/{}".format(LogDestBase, caseNumber, firstfilename)):
                        printDLSize(downloadURL)
                        urllib.urlretrieve(text[24:], os.path.join("{}/{}".format(LogDestBase, caseNumber), firstfilename))
            except:
                print "ERROR: Executing {} failed.".format(caseNumber)
                # cancel execution so not try to unzip if this download fails?
                # delete the

def printDLSize(downloadURL):
    openDL = urllib.urlopen("%s" % downloadURL)
    print "Currently downloading from S3: ", humanize.naturalsize((openDL.info()['Content-Length']))


def downloadFTP(caseNumber, ftpAddress):
    from ftplib import FTP

    ftpTargetDir = "{}/{}/FTP".format(LogDestBase, caseNumber)

    firstSplit = ftpAddress.split(":")
    ftpUsername = firstSplit[1][2:]
    # print caseNumber + " potentially problematic FTP split: ", firstSplit[2]
    secondSplit = firstSplit[2].split("@")
    ftpPassword = secondSplit[0]
    ftpDomain = secondSplit[1]

    try:
        ftp = FTP(ftpDomain)
        ftp.login(ftpUsername, ftpPassword)
        filenames = ftp.nlst() # get filenames within the ftp directory

        if filenames:
            if not os.path.exists("{}/{}/FTP".format(LogDestBase, caseNumber)):
                os.makedirs("{}/{}/FTP".format(LogDestBase, caseNumber))
            for filename in filenames:
                local_filename = os.path.join(ftpTargetDir, filename)
                if not os.path.exists(local_filename):
                    file = open(local_filename, 'wb')
                    "Currently downloading from FTP"
                    ftp.retrbinary('RETR '+ filename, file.write)
                    file.close()
                    # extract if .zip ?
            ftp.quit()
        else:
            # ftp is empty
            pass
    except:
        print "Exception: Problem connecting to FTP for %s." % caseNumber
        pass



if __name__ == "__main__":
    downloadLogs()
