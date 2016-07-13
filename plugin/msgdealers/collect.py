# coding=utf8


def collect(msg, storageClass=None, userName=None):
    str = '201'
    if str not in msg:
        return False
    storageClass.store_report(userName, msg)
    return False
