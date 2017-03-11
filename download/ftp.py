import os

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
