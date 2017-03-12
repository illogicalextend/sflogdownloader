import os
import urllib
import humanize

def printDLSize(downloadURL):
    openDL = urllib.urlopen("%s" % downloadURL)
    print "Currently downloading from S3: ", \
        humanize.naturalsize((openDL.info()['Content-Length']))

# if "amazonaws" is in the salesforce comment
def downloadS3(text, caseNumber, LogDestBase):
    downloadURL = text[24:]
    if "\n\n" not in text[24:] and len(text[24:]) < 220:
        firstfilename = text[24:].split('/')[-1].split('#')[0].split('?')[0]
        caseNumberPath = "{}/{}/{}".format \
            (LogDestBase, caseNumber, firstfilename[:-4])
        if not os.path.exists("{}/{}/{}/{}".format(LogDestBase, caseNumber,
            firstfilename[:-4], firstfilename)):
            try:
                if firstfilename[-4:] == ".zip":
                    # create directory (if doesn't exist) to store contents of
                    #zip, by trimming ".zip" and naming directory after filename
                    if not os.path.exists(caseNumberPath):
                        os.makedirs(caseNumberPath)
                    # download full .zip file path to newly created directory
                    printDLSize(downloadURL)
                    urllib.urlretrieve(text[24:], \
                                       os.path.join("{}/{}". \
                                                    format(caseNumberPath,
                                                           firstfilename)))
                    os.system("unzip -o -q {}/{} -d {}".format(caseNumberPath,
                                                               firstfilename,
                                                               caseNumberPath))
                else:
                    # else if not .zip, download other type of file \
                    # and don't try to extract it.
                    if not os.path.exists("{}/{}/{}".format(LogDestBase,
                                                            caseNumber,
                                                            firstfilename)):
                        printDLSize(downloadURL)
                        urllib.urlretrieve(text[24:], os.path.join("{}/{}". \
                            format(LogDestBase, caseNumber), firstfilename))
            except Exception as e:
                print "ERROR: Executing {} failed.".format(caseNumber)
                print str(e)
                # cancel execution so not try to unzip if this download fails?


def downloadFTP(caseNumber, ftpAddress, LogDestBase):
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
                    print "Currently downloading from FTP"
                    ftp.retrbinary('RETR '+ filename, file.write)
                    file.close()
                    # extract if .zip ?
            ftp.quit()
        else:
            # ftp is empty
            pass
    except Exception as e:
        print "Exception: Problem connecting to FTP for %s." % caseNumber
        print str(e)
        pass
