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
        if not os.path.exists("{}/{}/{}/{}".format(LogDestBase, caseNumber,
            firstfilename[:-4], firstfilename)):
            try:
                if firstfilename[-4:] == ".zip":
                    # create directory (if doesn't exist) to store contents of
                    #zip, by trimming ".zip" and naming directory after filename
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
            except Exception as e:
                print "ERROR: Executing {} failed.".format(caseNumber)
                print str(e)
                # cancel execution so not try to unzip if this download fails?
