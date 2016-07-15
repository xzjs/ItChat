# -*- coding:utf-8 -*-
import time

from plugin.Sqlite3Client import Sqlite3Client


def collect(msg, storageClass=None, userName=None):
    str = '201'
    if str in msg:
        storageClass.store_report(userName, msg)
    str == u'report'
    if str in msg:
        a = analyse()
        text = a.get_sentence()
        return text
    if int(msg) > 1 and int(msg) < 9999999:
        a = analyse()
        text = a.liu(msg)
        return text
    return False


class analyse:
    def __init__(self):
        self.str = u'网络所(' + time.strftime('%Y%m%d') + u')网络所工作汇报:平行网络和车联网相关研究推进;'
        self.names = [[u'李静', u'要婷婷', u'宋瑞琦', u'郭奇', u'温纪庆', u'胡成云', u'王迎春'], [u'刘全杰'], [u'李茂双', u'王金慧', u'孙玉秀'],
                      [u'晏西国'],
                      [u'王晶']]
        self.strs = [u'无人车项目推进:', u'停车项目推进:', u'(前端)', u'(后台)', u'手机信令项目推进:']

    def get_dict(self, names=None):
        """ 将数据库中的语句生成字典 """
        dict = {}
        for name in names:
            with Sqlite3Client('storage/account/血之君殇.db') as s3c:
                # todo:这里应该搜索时间为今天的汇报
                messages = s3c.query('select * from report WHERE UserName =? order by time desc', (name,))
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
        """ 获得最后的拼装语句 """
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

    def liu(self, msg):
        id_list = list(msg)
        user_list = []
        for id in id_list:
            with Sqlite3Client('storage/account/血之君殇.db') as s3c:
                user = s3c.query('select * from member WHERE id =?', (id,))[0][1]
                user_list.append(user)
        dict = self.get_dict(user_list)
        str = ''
        for key in dict.keys():
            str += key + ':' + ','.join(dict[key]) + '\n'
        return str;


class report:
    def __init__(self, s, nickname, client, time_str='220000'):
        self.s = s
        self.nickname = nickname
        self.client = client
        self.time_str = time_str
        self.username = self.s.find_user(self.nickname)

    def do(self):
        time_str = time.strftime('%H%M%S')
        print time_str
        if time_str == self.time_str:
            a = analyse()
            msg = a.get_sentence()
            self.client.send_msg(self.username, msg)
