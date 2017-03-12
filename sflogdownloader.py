#!/usr/bin/env python

from process import getCasesContent
from process import authSalesforce
import os

# destination for log downloads
LogDestBase = "/vagrant/project/flaskapp/logs1"

# salesforce user owner id. To return multiple,
# set to "OwnerId = 'x' or OwnerId = 'y'"
sfOwnerId = "00532000004yymVAAQ"

def createLogDir():
    if not os.path.exists(LogDestBase):
        os.makedirs(LogDestBase)


if __name__ == "__main__":
    sf = authSalesforce()
    createLogDir()
    getCasesContent(sf, LogDestBase, sfOwnerId)
