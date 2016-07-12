# coding=utf8

def collect(msg, storageClass=None, userName=None):
    if u'智能网络研究所个人工作汇报' not in msg:
        return False
    storageClass.store_report(userName, msg)
    return False
