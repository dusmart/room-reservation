import logging
import sys
import requests
from datetime import date, timedelta, datetime
import re
from bs4 import BeautifulSoup
import random
import time

LOGGER = logging.getLogger()
_HANDLER = logging.StreamHandler()
_HANDLER.setFormatter(logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
LOGGER.addHandler(_HANDLER)
LOGGER.setLevel(logging.DEBUG)
LOGGER.setLevel(logging.INFO)
#LOGGER.setLevel(logging.WARNING)

class Student:
    def __init__(self, memberid):
        """根据学生id模拟其登陆图书馆主页，并开启相关会话
        """
        self.memberid = memberid
        self.MAIN_PAGE = 'http://studyroom.lib.sjtu.edu.cn'
        self.RESERVE_PAGE = 'http://studyroom.lib.sjtu.edu.cn/reserve_add.asp'
        self.LIST_PAGE = 'http://studyroom.lib.sjtu.edu.cn/user_reserve_list.asp'
        self.APPLY = 'http://studyroom.lib.sjtu.edu.cn/reserve_plus_ok.asp'
        self.JASiteCookies=[
              'CJALMzLoXByYqrBtDZ7%2BnabRLXpFQMSvjyu38MuNE29ULaVzeR5eZeUOTLmuXGTklbnq4iW043LkB9s3I62CWUJn8YeHf%2F%2BesnLmExvhL2ETIjMIWymXDc6PPNi8FtYK3e5dtswZ3kLVX%2BF42qrSpl0dShqxNhKOGbLilacHH7azUN4VjPT%2BbaXeFqWH6SBiSLMX2P1NYipdxx%2FdTc8tgZwkaXnnEg%2B7ruGACZ6VZYyAbp0JXIWzVbHm7dqosvEj5omgUnP1Iee1CF5yHJYLIguf1PCDgvYX5wmLgEVOam0p2oCS98n%2BJ5m7tAZKvmmXkgbYfBmRUc9mUnTQANe3de8vwdmoUElwm3V96qSipTFDAAZl3Djsji7FlYYjeRf7QRC%2B57R7pffgkDlAtl1ZnPRFUdJq3I6l9A%3D%3D',
              'CLrWsKhVhoJxvoRLhDUPQ1GiTsdAcRmLefMwq%2FmJiaL40GH8XQJ7GDGFNFIWbwPwdOoa6KAkFCCmuEoncEcJ%2B5MReE5IC%2FnkN7d%2BSxNxbh%2FDORRKlpf92f2ryQ67%2FgKgkgXBz1ONFXr6kK1%2Fo3WguVB2OZytkMz5TYD0aXjO9RuqLTmR271OthJ5yYQ76vxsH%2FrNicGfKeu1r%2Fr3ddkq9N9F8k96yrx%2Fn%2BCzuniNfv49xbbS6RwbbLThmLM5wb1FhtNmjNIi%2F9o6y2xHcgNy82MyLA63qa7s2axMmkj%2BFA7Nytl%2FqG1YDoFFrNZkY0WBAT3XHz8dok24FpxCo%2Fg3odglPpC4Dwv4L%2FLNm6zPJe3axYU4wXzuHaIi3Dp4FgEyAkALlYnC7STvO5qwggIN6VBdoTJ7sLwKrOO4HgCMz7dPOkesQgNGydk%3D',
              'CBKl3ILfCVTIPdwvl8yU4pvlSGAcRLJmclAE1tDlfEAfKoB0si5cICJOHcDzCoGg57UngZGHD4tUNNqHKHYTywcn5B8vINDLnLtcz%2BjZBqvQWRoPXEZljAIhqNutxnDL2%2BcG0WqvYjFcau498ZoFeH1AWgoQqskp5MChiKppSQCbIzeAQCSQvzU1eoYqEWY0pISpkqD8Z%2BqGiWSfQMIPBuYZ5r7yyK39DwlEkApksPUk4Zhb0xJyC%2B8sCF3WHjheMHeV%2Bx2M%2F444G2K68CnfJNUcQD%2FSA%2FoRVeJjVJYRmr%2BATSOt2I5xkhgQexPkRBlTQkwxBWYCfiz5qPOiiUgJBKOJYyMKz%2FQBox14%2Bf1WwekX5jLzCLygpHXNuTnulxzgFmRG%2BKzdMve0iYIPDEsYkggv3mdA83%2FIUg%3D%3D',
              ]
        self.ROOM_ID2NAME = {5: 'A315', 4: 'A316', 21: 'A415', 16: 'A416', 1: 'B215', 15: 'B216', 2: 'B315', 19: 'B316', 20: 'B415', 3: 'B416', 11: 'C315', 12: 'C316', 9: 'E210', 22: 'E211', 23: 'E216', 24: 'E309', 7: 'E310', 8: 'E311', 25: 'E312', 26: 'E316', 6: 'A216'}
        self.ROOM_NAME2ID = {'A315': 5, 'A316': 4, 'A415': 21, 'A416': 16, 'B215': 1, 'B216': 15, 'B315': 2, 'B316': 19, 'B415': 20, 'B416': 3, 'C315': 11, 'C316': 12, 'E210': 9, 'E211': 22, 'E216': 23, 'E309': 24, 'E310': 7, 'E311': 8, 'E312': 25, 'E316': 26, 'A216': 6}
        self.GROUP_NAMES = ['自然语言处理小组', '图像识别小组', '音乐鉴赏讨论组', '数学分析交流', '线性代数讨论组', '自然语言处理小组']
        self.TOPIC_NAMES = ['自然语言处理+词性标注', '图像识别+损失函数讨论', '音乐鉴赏讨论+巴洛克器乐', '数学分析交流+二重积分', '线性代数讨论+矩阵求导', '自然语言处理+语义角色标注']
        self.DETAILS = ['词性标注实验结果分析（SVM和CRF）', '图像识别（由y和y_predict如何定义loss function较好）', '独奏协奏曲《春》的分析', '二重积分的技巧讨论', '矩阵求导+backpropagation', '自然语言处理小组+srl论文交流']

        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        self.session.cookies['JASiteCookie'] = self.JASiteCookies[memberid]
        self.session.get(self.MAIN_PAGE)

    def try_to_borrow(self, roomid_or_name, date_s, tstart, tend):
        """根据所申请的房间号，日期，开始/结束时间，组名，讨论话题，讨论内容尝试借取该讨论室
        如果成功借到则返回True，否则返回False，并在日志中记录失败或成功的信息
        """
        success = '预约成功'
        roomid = roomid_or_name if type(roomid_or_name)==int else self.ROOM_NAME2ID[roomid_or_name]
        roomname = self.ROOM_ID2NAME[roomid]
        LOGGER.info('尝试借阅\t人员id: %d\troomname:%s\tdate:%s\ttstart:%s\ttend:%s', self.memberid, roomname, date_s, tstart, tend)
        idx = random.randint(0,len(self.GROUP_NAMES)-1)
        groupname = self.GROUP_NAMES[idx]
        topic = self.TOPIC_NAMES[idx]
        detail = self.DETAILS[idx]
        payload = {'roomid': roomid, 'tstart': date_s+" "+tstart, 'tend': date_s+" "+tend,\
                            'groupname': groupname, 'topic': topic, 'detail':detail, 'attendcount':'3',\
                            'partake':'1', 'specialneed':'','action':'post', 'B1':'提交'}
        ideal_room = self.session.post(self.RESERVE_PAGE, data=payload)
        ideal_room.encoding = 'utf-8'
        if success in ideal_room.text:
            LOGGER.info('申请借阅成功\t人员id: %d\troomname:%s', self.memberid, roomname)
        else:
            soup = BeautifulSoup(ideal_room.text, "html.parser")
            try:
                reason = soup.body.find_all(attrs={"class": "main row"})[0].script.getText().split("'")[1]
            except:
                reason = "Unknown reason"
            LOGGER.info('申请借阅失败\t人员id: %d\troomname:%s\treason:%s', self.memberid, roomname, reason)
        return success in ideal_room.text

    def get_id_pass(self):
        """获取该学生已经借到的讨论室的申请单号、房间名和加入该房间所需的密码
        """
        borrowed_room = self.session.get(self.LIST_PAGE)
        borrowed_room.encoding = 'utf-8'
        soup = BeautifulSoup(borrowed_room.text, "html.parser")
        table = soup.body.table
        info = table.find_all('tr')
        result = []
        for tr in info:
            if '密码' in tr.getText():
                td = tr.find_all('td')
                applicationid = td[1].getText()
                password = td[-2].getText()[-7:-1]
                roomname = td[4].getText()
                result.append([applicationid, password, roomname])
        return result

    def apply(self, applicationid, password, roomname):
        """根据申请单号、密码和房间名，加入已申请的讨论室
        """
        success = '加入申请成功'
        payload = {'password':password,'B1':'加入','applicationid':applicationid,\
                    'needusernum':2, 'roomname':roomname}
        result = self.session.post(self.APPLY, data=payload)
        result.encoding = 'utf-8'
        if success in result.text:
            LOGGER.info('申请加入成功\t人员id: %d\troomname:%s', self.memberid, roomname)
        else:
            LOGGER.info('申请加入失败\t人员id: %d\troomname:%s', self.memberid, roomname)
        return success in result.text



# 实际中其他数字也可以，您可以试试1-30，建议只从以下id中选讨论室
VISIBLE_ROOMIDS = [1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 15, 16, 19, 20, 21, 22, 23, 24, 25, 26, 6]


def borrow(apply_date,start,room="any",duration=4):
    """
        配置借图书馆的策略，需要日期、开始时间，可选房间名、借讨论室时长
    """
    english2date = {'today': 0, 'tommorrow': 1}
    weekday = ['mon', 'tues', 'wed', 'thur', 'fri', 'sat', 'sun']
    if apply_date in english2date:
        apply_date = english2date[apply_date]
        date_s = date.isoformat(date.today()+timedelta(days = apply_date))
    elif type(apply_date) == str and apply_date.lower() in weekday:
        apply_date = (weekday.index(apply_date.lower()) - (datetime.now().weekday()) + 7) % 7
        date_s = date.isoformat(date.today()+timedelta(days = apply_date))
    elif apply_date.isdigit():
        date_s = date.isoformat(date.today()+timedelta(days = int(apply_date)))
    else:
        date_s = date.isoformat(apply_date)
    if start - int(start) < 0.001:
        tstart = '{:0>2d}:00'.format(int(start))
        tend = '{:0>2d}:00'.format(min(23, int(start)+duration))
    else:
        tstart = '{:0>2d}:30'.format(int(start))
        if int(start)+duration < 23:
            tend = '{:0>2d}:30'.format(int(start)+duration)
        else:
            tend = '23:00'
    leader = Student(0)

    if room != "any":
        leader.try_to_borrow(room, date_s, tstart, tend)
    else:
        for roomid in VISIBLE_ROOMIDS:
            succ = leader.try_to_borrow(roomid, date_s, tstart, tend)
            if succ:
                break
        if not succ:
            LOGGER.warning("我已经尽力了，然而就是借不到讨论室")
    return leader.get_id_pass()



def apply(applicationid, password, roomname):
    member1 = Student(1)
    member1.apply(applicationid, password, roomname)
    member2 = Student(2)
    member2.apply(applicationid, password, roomname)

def main():
    if len(sys.argv) == 1:
        infos = borrow('today',time.localtime(time.time())[3],'any')
    elif len(sys.argv) == 2:
        infos = borrow(sys.argv[1],time.localtime(time.time())[3],'any')
    elif len(sys.argv) == 3:
        infos = borrow(sys.argv[1],float(sys.argv[2]),'any')
    elif len(sys.argv) == 4:
        infos = borrow(sys.argv[1],float(sys.argv[2]),sys.argv[3])
    elif len(sys.argv) == 5:
        infos = borrow(sys.argv[1],float(sys.argv[2]),sys.argv[3],int(sys.argv[4]))
    for applicationid, password, roomname in infos:
        apply(applicationid, password, roomname)

if __name__ == "__main__":
    main()
