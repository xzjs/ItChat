# -*- coding:utf-8 -*-
import os
import time

from itchat import config
from plugin.Sqlite3Client import Sqlite3Client


class reportAnaylze:
    def __init__(self):
        self.str = u'网络所(' + time.strftime('%Y%m%d') + u')网络所工作汇报:平行网络和车联网相关研究推进;'
        self.names = [[u'李静', u'要婷婷', u'宋瑞琦', u'郭奇', u'温纪庆', u'胡成云', u'王迎春'], [u'刘全杰'], [u'李茂双', u'王金慧', u'孙玉秀'],
                      [u'晏西国'],
                      [u'王晶']]
        self.strs = [u'无人车项目推进:', u'停车项目推进:', u'(前端)', u'(后台)', u'手机信令项目推进:']
        self.sqlDir = os.path.join(config.ACC_DIR, 'reportdb.db')
        with Sqlite3Client(self.sqlDir) as s3c:
            s3c.execute(
                'create table if not exists reports (message text(128),nickname text(128),time double(128))')
            s3c.execute('create table if not exists my_reports(message text,time integer)')
            s3c.execute(
                'create table if not exists my_reports(id integer,name text(128))')

    def collect(self, msg):
        if u'\u5de5\u4f5c\u6c47\u62a5' in msg['Content']:
            with Sqlite3Client(self.sqlDir) as s3c:
                s3c.insert_data('reports',
                                [msg['Content'], msg['ActualNickName'], int(time.time())])

    def auto_report(self, itchat):
        chatroomname = 'test'
        chatrooms = itchat.get_chatrooms()
        for chatroom in chatrooms:
            if chatroom['PYQuanPin'] == chatroomname:
                itchat.send_msg('hello', chatroom['UserName'])
                break

    def get_dict(self, names=None):
        """ 将数据库中的语句生成字典 """
        dict = {}
        for name in names:
            with Sqlite3Client(self.sqlDir) as s3c:
                messages = s3c.query('select * from reports WHERE nickname =? order by time desc', (name,))
                if len(messages):
                    messagelist = (messages[0][0])[5:]
                    dict[name] = messagelist.strip()
        return dict

    def get_sentence(self):
        """ 获得最后的拼装语句 """
        for i in range(0, len(self.names)):
            for value in self.get_dict(self.names[i]).values():
                self.strs[i] += value + ','
        self.str += ''.join(self.strs)
        return self.str

    def liu(self):
        user_list = [u'李茂双', u'孙玉秀', u'王金慧', u'刘全杰']
        dict = self.get_dict(user_list)
        str = ''
        for key in dict.keys():
            str += key + ':' + dict[key] + '\n'
        return str
