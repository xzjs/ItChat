# -*- coding:utf-8 -*-
import re

import time

import thread

from plugin.Sqlite3Client import Sqlite3Client


class analyse:
    def __init__(self):
        self.str = u'网络所(' + time.strftime('%Y%m%d') + u')网络所工作汇报:平行网络和车联网相关研究推进;'
        self.names = [[u'李静', u'要婷婷', u'宋瑞琦', u'郭奇', u'温纪庆', u'胡成云', u'王迎春'], [u'刘全杰'], [u'李茂双', u'王金慧', u'孙玉秀'],
                      [u'晏西国'],
                      [u'王晶']]
        self.strs = [u'无人车项目推进:', u'停车项目推进:', u'(前端)', u'(后台)', u'手机信令项目推进:']

    def get_dict(self, names=None):
        dict = {}
        for name in names:
            with Sqlite3Client('storage/account/血之君殇.db') as s3c:
                # todo:这里应该搜索时间为今天的汇报
                messages = s3c.query('select * from report WHERE UserName =?', (name,))
                if len(messages):
                    messagelist = (messages[0][1]).split('<br/>')[1:]
                    dict[name] = []
                    for m in messagelist:
                        if m != '':
                            m_list = list(m)
                            temp = []
                            for word in m_list:
                                if word not in u'(123456789). ）（。':
                                    temp.append(word)
                            dict[name].append(''.join(temp))
        return dict

    def get_sentence(self):
        for i in range(0, len(self.names)):
            for value in self.get_dict(self.names[i]).values():
                for sentence in value:
                    if sentence != '':
                        self.strs[i] += sentence + ','
        self.str += ''.join(self.strs)
        l = list(self.str)
        l[-1] = '.'
        self.str = ''.join(l)
        return self.str


class mytime:
    def __init__(self, h=22, m=0, s=0):
        self.h = h
        self.m = m
        self.s = s

    def func(self):
        while True:
            print 'func run'
            time.sleep(1)

    def main_func(self):
        thread.start_new_thread(self.func, ())
        while True:
            print 'main run'
            time.sleep(2)


class report:
    def __init__(self, s, nickname, client):
        self.s = s
        self.nickname = nickname
        self.client = client

    def do(self):
        username = self.s.find_user(self.nickname)
        self.client.send_msg(username)
