from simple_salesforce import Salesforce

def authSalesforce():
    with open('credentials.txt') as f:
        lines = f.read().splitlines()
        sfUsername = lines[0]
        sfPassword = lines[1]
        sfToken = lines[2]
        sf = Salesforce(username='%s' % sfUsername, password='%s' % sfPassword, security_token='%s' % sfToken)
        return sf
