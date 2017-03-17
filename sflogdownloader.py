#!/usr/bin/env python

from process import get_process_case
from process import authSalesforce
from process import logRetention
import os

# destination for log downloads
LogDestBase = "/vagrant/project/flaskapp/logs1"

# salesforce user owner id. To return multiple,
# set to "OwnerId = 'x' or OwnerId = 'y'"
sfOwnerId = "00532000004yymVAAQ"

# number of days to store logs before deleting them.
savedFilesRetention = 40

def createLogDir():
    if not os.path.exists(LogDestBase):
        os.makedirs(LogDestBase)


if __name__ == "__main__":
    sf = authSalesforce()
    createLogDir()
    get_process_case(sf, LogDestBase, sfOwnerId)
    logRetention(LogDestBase, savedFilesRetention)
