from auth import authSalesforce

def getSalesforceCases(LogDestBase, sfOwnerId):
     print "Destination: {}".format(LogDestBase)
     print "Checking for available logs.."
     caseListResult = "SELECT CaseNumber, Status, Case_External_ID__c, \
        LogLocationFTPURL__c FROM Case where (Status != 'closed' and \
        Status != 'Closed No Response' and Status != 'Merged' and \
        Status != 'Junk' and Status != 'Closed by Customer' and \
        Status != 'Closed In KB' and Status != 'Call No-Answer') and \
        (OwnerId = '%s') ORDER BY CaseNumber ASC" % sfOwnerId
     query = authSalesforce().query(caseListResult)
     records = query['records']
     return records
