

from auth import authSalesforce

def getSalesforceCases(LogDestBase):
     print "Destination: {}".format(LogDestBase)
     print "Checking for available logs.."
     #caseListResult = "SELECT CaseNumber, Status, Case_External_ID__c, LogLocationFTPURL__c FROM Case where (Status != 'closed' and Status != 'Closed No Response' and Status != 'Merged' and Status != 'Junk' and Status != 'Closed by Customer' and Status != 'Closed In KB' and Status != 'Call No-Answer') and (OwnerId = '00532000004yymVAAQ' or OwnerId = '00532000003hdv9AAA' or OwnerId = '00532000003i25wAAA' or OwnerId = '00532000004ytb3AAA' or OwnerId = '00532000004yymaAAA' or OwnerId = '00532000004z91pAAA' or OwnerId = '00532000004zGNxAAM' or OwnerId = '00532000004zXpjAAE' or OwnerId = '00532000004zcz0AAA' or OwnerId = '00532000004zkB3AAI' or OwnerId = '00532000005NPnsAAG' or OwnerId = '00532000005UlUNAA0' or OwnerId = '00532000005UlUSAA0' or OwnerId = '00532000005UlUXAA0' or OwnerId = '00532000005V37vAAC' or OwnerId = '005600000029jF0AAI' or OwnerId = '00560000002AsvZAAS' or OwnerId = '00560000003X9XRAA0' or OwnerId = '00560000003XehPAAS') ORDER BY CaseNumber ASC"
     caseListResult = "SELECT CaseNumber, Status, Case_External_ID__c, LogLocationFTPURL__c FROM Case where (Status != 'closed' and Status != 'Closed No Response' and Status != 'Merged' and Status != 'Junk' and Status != 'Closed by Customer' and Status != 'Closed In KB' and Status != 'Call No-Answer') and (OwnerId = '00532000004yymVAAQ') ORDER BY CaseNumber ASC"
     query = authSalesforce().query(caseListResult)
     records = query['records']
     return records
