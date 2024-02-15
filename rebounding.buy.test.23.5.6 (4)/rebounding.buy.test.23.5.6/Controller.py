import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from Savedstockitem import *
from re_main import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
from multiprocessing import Queue
import random

import win32com.client
import pythoncom

import time

import xing_login

import win32com.client
import pythoncom
import os, sys
import inspect
from PyQt5.QtTest import *
import threading
from PyQt5.QtCore import QTime


class Sig_cl(QObject): #시그널용 클래스
    sig_ = pyqtSignal() #시그널 생성 객체

    def signal_(self):
        self.sig_.emit() #시그널 생성


class XSession:
    """
    classmethod get_instance() 를 사용하여, instance 를 만들어야함.
    """
    def __init__(self):
        self.login_state = 0

    def OnLogin(self, code, msg):  # event handler
        """
        Login 이 성공적으로 이베스트 서버로 전송된후,
        로그인 결과에 대한 Login 이벤트 발생시 실행되는 event handler
        """
        if code == "0000":
            print("로그인 ok\n")
            self.login_state = 1
            self.account_info()
        else:
            self.login_state = 2
            print("로그인 fail.. \n code={0}, message={1}\n".format(code, msg))

    def api_login(self, id="soni4589", pwd="vcxz1245", cert_pwd="vcxz1245!!"): # id, 암호, 공인인증서 암호
        self.ConnectServer("hts.ebestsec.co.kr", 20001) # 모의투자 "demo.ebestsec.co.kr"
        is_connected = self.Login(id, pwd, cert_pwd, 0, False)  # 로그인 하기

        if not is_connected:  # 서버에 연결 안되거나, 전송 에러시
            print("로그인 서버 접속 실패... ")
            return

        while self.login_state == 0:
            pythoncom.PumpWaitingMessages()

    def account_info(self):
        """
        계좌 정보 조회
        """
        if self.login_state != 1:  # 로그인 성공 아니면, 종료
            return

        account_no = self.GetAccountListCount()

        print("계좌 갯수 = {0}".format(account_no))

        for i in range(account_no):
            account = self.GetAccountList(i)
            print("계좌번호 = {0}".format(account))

    @classmethod
    def get_instance(cls):
        # DispatchWithEvents로 instance 생성하기
        xsession = win32com.client.DispatchWithEvents("XA_Session.XASession", cls)
        return xsession


class XQuery_t1101:
    def __init__(self):
        super().__init__()
        self.is_data_received = False

    def OnReceiveData(self, tr_code):
        """
        이베스트 서버에서 ReceiveData 이벤트 받으면 실행되는 event handler
        """
        self.is_data_received = True
        name = self.GetFieldData("t1101OutBlock", "hname", 0)
        price = self.GetFieldData("t1101OutBlock", "price", 0)
        volume = self.GetFieldData("t1101OutBlock", "volume", 0)



    def request(self, tcode):
        """
        이베스트 서버에 일회성 TR data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1101.res"  # RES 파일 등록
        self.SetFieldData("t1101InBlock", "shcode", 0, tcode)  # 삼성전자.
        err_code = self.Request(False)  # data 요청하기 --  연속조회인경우만 True

        while self.is_data_received == False:
            pythoncom.PumpWaitingMessages()

        name = self.GetFieldData("t1101OutBlock", "hname", 0)

        return name

        if err_code < 0:
            print("error... {0}".format(err_code)) # data 요청하기 --  연속조회인경우만 True

    @classmethod
    def get_instance(cls):
        xq_t1101 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return xq_t1101


class t1102(QAxWidget, QThread):
    def __init__(self):
        super().__init__()
        self.is_data_received = False
        self.sig_cl = Sig_cl()
        self.savedstockitem = Savedstockitem()

    def OnReceiveData(self, code):
        """
        이베스트 서버에서 ReceiveData 이벤트 받으면 실행되는 event handler
        """


        self.is_data_received = True
        # self.savedstockitem.item_jango[stock_code] = ['', '', '', '']
        if code == "t1102":

            # cts_expcode = self.GetFieldData("t0424OutBlock", "cts_expcode", 0)
            # occurs_count = self.GetBlockCount("t0424OutBlock1")

            expcode = self.GetFieldData("t1102OutBlock", "shcode", 0)


            if expcode in self.savedstockitem.item_jango.keys():
                self.savedstockitem.item_jango[expcode][16] = self.GetFieldData("t1102OutBlock", "open", 0)

            try:
                # tt = self.savedstockitem.item_jango[expcode]
                self.savedstockitem.item_view[expcode][0] = str(expcode) #코드
                self.savedstockitem.item_view[expcode][1] = str(self.GetFieldData("t1102OutBlock", "hname", 0)) #종목명
                self.savedstockitem.item_view[expcode][2] = str(self.GetFieldData("t1102OutBlock", "price", 0)) #현재가
                self.savedstockitem.item_view[expcode][3] = self.GetFieldData("t1102OutBlock", "open", 0) #시가
                self.savedstockitem.item_view[expcode][4] = self.GetFieldData("t1102OutBlock", "high", 0) #고가
                # self.savedstockitem.item_view[expcode][5] = self.GetFieldData("t1102OutBlock", "low", 0) #반등폭
                self.savedstockitem.item_view[expcode][6] = self.GetFieldData("t1102OutBlock", "jkrate", 0) #신용여부

                if self.savedstockitem.item_view[expcode][6] == "":
                    self.savedstockitem.item_view[expcode][6] = '0'

            except:
                self.sig_cl.signal_()


        self.sig_cl.signal_()
        #print(self.savedstockitem.Save())


        a = self.GetFieldData("t1102OutBlock", "open", 0)

        print(a)
        #return (a)

    def request(self, tcode):
        """
        이베스트 서버에 일회성 TR data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1102.res"  # RES 파일 등록
        self.SetFieldData("t1102InBlock", "shcode", 0, tcode)  # 삼성전자.
        err_code = self.Request(False)  # data 요청하기 --  연속조회인경우만 True


        while self.is_data_received == False:
            pythoncom.PumpWaitingMessages()

        # name = self.GetFieldData("t1102OutBlock", "hname", 0)
        #
        # return name

        if err_code < 0:
            print("error... {0}".format(err_code)) # data 요청하기 --  연속조회인경우만 True

    @classmethod
    def get_instance(cls):
        xq_t1102 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return xq_t1102


class t0424(QAxWidget, QThread):
    def __init__(self):
        super().__init__()
        self.is_data_received = False
        self.sig_cl = Sig_cl()
        self.savedstockitem = Savedstockitem()
        self.t1102 = t1102.get_instance()

    def OnReceiveData(self, code):
        print("%s 수신" % code, flush=True)
        self.is_data_received = True
        #self.savedstockitem.item_jango[stock_code] = ['', '', '', '']
        if code == "CSPAQ12300":

            #cts_expcode = self.GetFieldData("t0424OutBlock", "cts_expcode", 0)
            #occurs_count = self.GetBlockCount("t0424OutBlock1")

            occurs_count = self.GetBlockCount("CSPAQ12300OutBlock3")
            tt = None

            try:
                for cc in self.savedstockitem.item_jango.keys():
                    if self.savedstockitem.item_jango[cc][14] == 0:
                        del self.savedstockitem.item_jango[cc]
            except:
                pass

            for i in range(occurs_count):

                expcode = self.GetFieldData("CSPAQ12300OutBlock3", "IsuNo", i)

                expcode = str(expcode[1:])



                try:
                    if expcode in self.savedstockitem.item_view.keys():
                        result_code = self.savedstockitem.item_view[expcode][14]
                        print(result_code)
                        if result_code == 0:
                            if expcode not in self.savedstockitem.item_jango.keys():
                                self.savedstockitem.item_jango[expcode] = ['', '', '', '', '', '', '', '9999999', '0', '9999999', '0','퍼샌트익절가','익절선택','손절선택', '2' ,'최저점','당일시가']
                        else:
                            if expcode not in self.savedstockitem.item_jango.keys():
                                self.savedstockitem.item_jango[expcode] = ['', '', '', '', '', '', '', '9999999', '0',
                                                                           '9999999', '0', '퍼샌트익절가', '익절선택', '손절선택',
                                                                           '2', '최저점', '당일시가']

                            #익절선택 자동 2 수동 1 퍼센트 0 / 손절 선택 자동 2 수동 1
                    else:

                        if expcode not in self.savedstockitem.item_jango.keys():
                            self.savedstockitem.item_jango[expcode] = ['', '', '', '', '', '', '', '9999999', '0',
                                                                       '9999999', '0', '퍼샌트익절가', '익절선택', '손절선택', '2',
                                                                       "최저점", '당일시가']



                except:

                    if expcode not in self.savedstockitem.item_jango.keys():
                        self.savedstockitem.item_jango[expcode] = ['', '', '', '', '', '', '', '9999999', '0',
                                                                   '9999999', '0', '퍼샌트익절가', '익절선택', '손절선택', '2',
                                                                   "최저점", '당일시가']


                #tt = self.savedstockitem.item_jango[expcode]
                self.savedstockitem.item_jango[expcode][0] = str(expcode)
                self.savedstockitem.item_jango[expcode][1] = str(self.GetFieldData("CSPAQ12300OutBlock3", "IsuNm", i))
                self.savedstockitem.item_jango[expcode][2] = str(self.GetFieldData("CSPAQ12300OutBlock3", "NowPrc", i))
                self.savedstockitem.item_jango[expcode][3] = self.GetFieldData("CSPAQ12300OutBlock3", "AvrUprc", i)
                self.savedstockitem.item_jango[expcode][4] = self.GetFieldData("CSPAQ12300OutBlock3", "BnsBaseBalQty", i)
                self.savedstockitem.item_jango[expcode][5] = self.GetFieldData("CSPAQ12300OutBlock3", "CrdtAmt", i)
                self.savedstockitem.item_jango[expcode][6] = self.GetFieldData("CSPAQ12300OutBlock3", "LoanDt", i)
                if self.savedstockitem.item_jango[expcode][6] == "":
                    self.savedstockitem.item_jango[expcode][6] = '0'



                self.t1102.request(expcode)

        self.sig_cl.signal_()

    def t0424_request(self, cts_expcode=None, next=None):

        """
        이베스트 서버에 일회성 TR data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CSPAQ12300.res"
        # RES 파일 등록
        """
        self.SetFieldData("t0424InBlock", "accno", 0, "20431636501")
        self.SetFieldData("t0424InBlock", "passwd", 0, "2072")
        self.SetFieldData("t0424InBlock", "prcgb", 0, "1")
        self.SetFieldData("t0424InBlock", "chegb", 0, "2")
        self.SetFieldData("t0424InBlock", "dangb", 0, "0")
        self.SetFieldData("t0424InBlock", "charge", 0, "1")
        self.SetFieldData("t0424InBlock", "cts_expcode", 0, cts_expcode )
        """

        self.SetFieldData("CSPAQ12300InBlock1", "RecCnt", 0, "00001")
        self.SetFieldData("CSPAQ12300InBlock1", "AcntNo", 0, "20431636501") # 모의투자  55500651101
        self.SetFieldData("CSPAQ12300InBlock1", "Pwd", 0, "2072") # 모의투자  0000
        self.SetFieldData("CSPAQ12300InBlock1", "BalCreTp", 0, "0")
        self.SetFieldData("CSPAQ12300InBlock1", "CmsnAppTpCode", 0, "0")
        self.SetFieldData("CSPAQ12300InBlock1", "D2balBaseQryTp", 0, "1")
        self.SetFieldData("CSPAQ12300InBlock1", "UprcTpCode", 0, "0")

        self.Request(False)

        while self.is_data_received == False:

            pythoncom.PumpWaitingMessages()

    @classmethod
    def get_instance(cls):
        t0424 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return t0424



class XReal_S3__(QAxWidget, QThread):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.sig_cl = Sig_cl()
        self.savedstockitem = Savedstockitem()
        self.order_stock = order_stock()


    def OnReceiveRealData(self, tr_code):  # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count = 1

        if tr_code == "S3_":
            self.scode = str(self.GetFieldData("OutBlock", "shcode"))
            self.time = self.GetFieldData("OutBlock", "chetime")
            self.price = int(self.GetFieldData("OutBlock", "price"))
            self.open = int(self.GetFieldData("OutBlock", "open"))
            self.high = int(self.GetFieldData("OutBlock", "high"))
            if self.price < 0:
                self.price = self.price * (-1)
            self.price_up_down = self.GetFieldData("OutBlock", "drate")
            self.volume = self.GetFieldData("OutBlock", "cvolume")
            self.hour = int(self.time) / 10000
            self.min = int(self.time) / 100 % 100
            self.sec = int(self.time) % 100
            self.csode = self.scode
            #self.scode = "A" + self.scode  # 모의투자 self.scode

            if self.scode in self.savedstockitem.item_jango.keys():
                self.savedstockitem.item_jango[self.scode][2] = str(self.price)
                self.savedstockitem.item_jango[self.scode][16] = str(self.open)

                sc = self.savedstockitem.item_jango[self.scode][9]  # 수동익절가
                asc = self.savedstockitem.item_jango[self.scode][7]  # 자동익절가
                fsc = float(sc)
                fasc = float(asc)
                sl = self.savedstockitem.item_jango[self.scode][10]  # 수동손절가
                asl = self.savedstockitem.item_jango[self.scode][8]  # 자동손절가
                fsl = float(sl)
                fasl = float(asl)
                l = self.savedstockitem.item_jango[self.scode][15]  # 최저점

                quanti = self.savedstockitem.item_jango[self.scode][4]  # 수량
                medo = 1

                try:
                    if int(self.savedstockitem.item_jango[self.scode][6]) != 0:
                        sss = 101
                        sssddd = self.savedstockitem.item_jango[self.scode][6]

                    else:
                        sss = "000"
                        sssddd = ""
                except:
                    pass


                try:
                    if int(self.savedstockitem.item_view[self.scode][14]) == 0:
                        self.savedstockitem.item_jango[self.scode][11] = 99
                        self.savedstockitem.item_jango[self.scode][12] = 2
                        self.savedstockitem.item_jango[self.scode][13] = 2

                    else:
                        self.savedstockitem.item_jango[self.scode][11] = 99
                        self.savedstockitem.item_jango[self.scode][12] = 1
                        self.savedstockitem.item_jango[self.scode][13] = 1
                except:
                    pass

                if self.savedstockitem.item_check["감시"] == 1:
                    if int(self.savedstockitem.item_jango[self.scode][14]) == 2:
                        if int(self.savedstockitem.item_jango[self.scode][12]) == 2:  # 익절선택-2자동
                            if (fasc <= self.price):  # 현재가 조건
                                self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                self.savedstockitem.item_jango[self.scode][14] = 0
                                print(self.scode + "익절선택-2자동")

                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 2:  # 손절선택-2자동
                                if (fasl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-2자동")

                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 1:  # 손절선택-1수동
                                if (fsl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-1수동")

                        elif int(self.savedstockitem.item_jango[self.scode][12]) == 1:  # 익절선택-1수동
                            if (fsc <= self.price):  # 현재가 조건
                                self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                self.savedstockitem.item_jango[self.scode][14] = 0
                                print(self.scode + "익절선택-1수동")
                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 2:  # 손절선택-2자동
                                if (fasl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-2자동")

                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 1:  # 손절선택-1수동
                                if (fsl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-1수동")

                        elif int(self.savedstockitem.item_jango[self.scode][12]) == 0:  # 익절선택-0퍼센트
                            p = self.savedstockitem.item_jango[self.scode][11]  # 프로익절가
                            ll = float(l) / 100 * (100 + float(p))
                            #fll = float(round(ll))
                            fll = int(round(float(ll)))

                            print(fll)
                            if (fll <= self.price):  # 현재가 조건
                                self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                self.order_stock.CSPAT00600_request(self.scode, quanti, medo, sss, sssddd)
                                self.savedstockitem.item_jango[self.scode][14] = 0
                                print(self.scode + "익절선택-0퍼센트")

                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 2:  # 손절선택-2자동
                                if (fasl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-2자동")

                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 1:  # 손절선택-1수동
                                if (fsl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-1수동")

                    # if (fsc <= self.price) or (fasc <= self.price) or (fsl > self.price) or (fasl > self.price):
                    #     self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                    #     print("매도 감시")


            if self.scode in self.savedstockitem.item_view.keys():
                self.savedstockitem.item_view[self.scode][2] = str(self.price)
                self.savedstockitem.item_view[self.scode][4] = str(self.high)
                self.savedstockitem.item_view[self.scode][3] = str(self.open)

                input_high = self.savedstockitem.item_view[self.scode][5]
                open_stock_code = self.savedstockitem.item_view[self.scode][7]
                volume_stock_code = self.savedstockitem.item_view[self.scode][8]
                high_stock_code = self.savedstockitem.item_view[self.scode][9]
                mesuprice_stock_code = self.savedstockitem.item_view[self.scode][12]
                qunti_stock_code = self.savedstockitem.item_view[self.scode][11]
                mesurate_stock_code = self.savedstockitem.item_view[self.scode][13]
                sinyung_stock_code = self.savedstockitem.item_view[self.scode][10]
                # result_stock_code = self.savedstockitem.item_view[self.scode][14]


                mesu = 2
                저 = float(self.savedstockitem.item_view[self.scode][26])
                고 = float(self.savedstockitem.item_view[self.scode][16])
                반등저점 = float(self.savedstockitem.item_view[self.scode][17])
                고돌거래량 = float(self.savedstockitem.item_view[self.scode][18])
                #고돌 = float(self.savedstockitem.item_view[self.scode][19])
                매수비율가 = float(((1 - (float(mesurate_stock_code) / 1000)) * (고 - 저)) + 저)
                폭 = float(self.savedstockitem.item_view[self.scode][20])
                반등폭2 = 2*폭
                
                sss = "000"
                sssddd = ""



                # 15 - 저, 16 - 고, 17 - 반등저점, 18 - 고돌거래량, 19 - 고돌, 20 - 매수비율가
                try:
                    if int(self.savedstockitem.item_view[self.scode][3]) < int(self.savedstockitem.item_view[self.scode][7]):

                        갭하락 = int(self.savedstockitem.item_view[self.scode][7]) - int(self.savedstockitem.item_view[self.scode][3])
                        if int(갭하락) > 반등폭2:
                            mesuprice_stock_code = float(mesuprice_stock_code) - 반등폭2
                            매수비율가 = 매수비율가 - 반등폭2
                except:
                    pass



                ooppen_time = QTime(9, 0, 0)
                market_start_time = QTime(9, 15, 0)
                open_time = QTime(10, 30, 0)
                middle_time = QTime(14, 0, 0)
                time_cule = int(self.savedstockitem.item_view[self.scode][23])
                current_time = QTime.currentTime()
                input_time = int(self.savedstockitem.item_view[self.scode][22])
                if float(mesuprice_stock_code) > 0:
                    input_price = float(mesuprice_stock_code)
                else:
                    input_price = 매수비율가
                  # 입력 매수가
                # lowest_price = 저
                # print(input_time)
                if input_time != 0:
                    print("input_time1")
                    if current_time <= open_time:
                        print("input_time11")
                        if 반등저점 > input_price:
                            self.savedstockitem.item_view[self.scode][23] = 1
                            time_cule = self.savedstockitem.item_view[self.scode][23]
                        else:
                            self.savedstockitem.item_view[self.scode][23] = 1
                            time_cule = self.savedstockitem.item_view[self.scode][23]
                            self.savedstockitem.item_view[self.scode][22] = 4

                    elif current_time < middle_time:
                        print("input_time111")
                        if current_time > open_time:

                            if 반등저점 > input_price:
                                self.savedstockitem.item_view[self.scode][23] = 2
                                time_cule = self.savedstockitem.item_view[self.scode][23]
                            else:
                                self.savedstockitem.item_view[self.scode][23] = 2
                                time_cule = self.savedstockitem.item_view[self.scode][23]
                                self.savedstockitem.item_view[self.scode][22] = 4


                    elif current_time >= middle_time:
                        print("input_time2")
                        if 반등저점 > input_price:
                            self.savedstockitem.item_view[self.scode][23] = 3
                            time_cule = self.savedstockitem.item_view[self.scode][23]
                            print("input_time3")
                        else:
                            print("input_time4")
                            self.savedstockitem.item_view[self.scode][23] = 3
                            time_cule = self.savedstockitem.item_view[self.scode][23]
                            self.savedstockitem.item_view[self.scode][22] = 4

                input_time = int(self.savedstockitem.item_view[self.scode][22])

                try:
                    if current_time >= ooppen_time:

                        if int(self.savedstockitem.item_view[self.scode][3]) < int(
                                self.savedstockitem.item_view[self.scode][7]):

                            print(self.savedstockitem.item_view[self.scode][3])
                            print(self.savedstockitem.item_view[self.scode][7])

                            if int(self.savedstockitem.item_view[self.scode][24]) == 1:  # 갭상승 매수하고 싶으면 1
                                self.savedstockitem.item_view[self.scode][14] = 0

                        if int(self.savedstockitem.item_view[self.scode][3]) >= int(
                                self.savedstockitem.item_view[self.scode][7]):

                            if int(self.savedstockitem.item_view[self.scode][24]) == 2:  # 갭하락 매수하고 싶으면 2
                                self.savedstockitem.item_view[self.scode][14] = 0
                except:
                    pass

                self.savedstockitem.item_view[self.scode][15] = 매수비율가


                bill_input = float(self.savedstockitem.item_view[self.scode][27])  # 입력한 글자 불러오는 메서드 text()

                mesu_input = float(매수비율가)

                # a = self.lineEdit.text()
                # print(self.savedstockitem.item_jango[self.scode][8])
                losep = (1 - (float(mesu_input) - (float(self.savedstockitem.item_view[self.scode][20]) * 2.3)) / float(
                    mesu_input)) * 100

                # now_num = self.savedstockitem.item_view[scode][2]

                # qunti = round(float(bill_input)/float(now_num))

                qunti_stock_code = round(float(bill_input) / float(mesu_input) / ((float(losep) / 100)))

                # 손절금 / 매수가 / (2 * (손절퍼센트 / 100))

                self.savedstockitem.item_view[self.scode][11] = qunti_stock_code

                print(self.savedstockitem.item_view[self.scode][11])

                if self.savedstockitem.item_check["감시"] == 1:  # 감지조건

                    if int(self.savedstockitem.item_view[self.scode][14]) >= 2:  # 종목별 감시결과조건

                        if int(self.savedstockitem.item_view[self.scode][13]) == 0:  # 매수비율조건

                            if (float(mesuprice_stock_code) >= self.price):  # 현재가 조건
                                if int(self.savedstockitem.item_view[self.scode][7]) >= 2:  # 전일종가 조건
                                    if int(self.savedstockitem.item_view[self.scode][9]) == 2:  # 거고돌
                                        if (고 > float(input_high)):
                                            if (고돌거래량 >= 1):
                                                if time_cule == 0:
                                                    self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code,
                                                                                        mesu,sss,sssddd)
                                                    if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                        self.savedstockitem.item_view[self.scode][14] = 1
                                                        print(self.scode + "거고돌")
                                                    else:
                                                        self.savedstockitem.item_view[self.scode][14] = 0
                                                        print(self.scode + "거고돌")


                                                elif time_cule == input_time:
                                                    self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code,
                                                                                        mesu,sss,sssddd)
                                                    if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                        self.savedstockitem.item_view[self.scode][14] = 1
                                                        print(self.scode + "거고돌")
                                                    else:
                                                        self.savedstockitem.item_view[self.scode][14] = 0
                                                        print(self.scode + "거고돌")




                                    elif int(self.savedstockitem.item_view[self.scode][8]) == 2:  # 거노고돌
                                        if (고 > float(input_high)):
                                            if current_time >= market_start_time:
                                                if (고돌거래량 < 1):

                                                    if time_cule == 0:
                                                        self.order_stock.CSPAT00600_request(self.scode,
                                                                                            qunti_stock_code, mesu,sss,sssddd)
                                                        if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                            self.savedstockitem.item_view[self.scode][14] = 1
                                                            print(self.scode + "거노고돌")
                                                        else:
                                                            self.savedstockitem.item_view[self.scode][14] = 0
                                                            print(self.scode + "거노고돌")



                                                    elif time_cule == input_time:
                                                        self.order_stock.CSPAT00600_request(self.scode,
                                                                                            qunti_stock_code, mesu,sss,sssddd)
                                                        if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                            self.savedstockitem.item_view[self.scode][14] = 1
                                                            print(self.scode + "거노고돌")
                                                        else:
                                                            self.savedstockitem.item_view[self.scode][14] = 0
                                                            print(self.scode + "거노고돌")




                                    elif int(self.savedstockitem.item_view[self.scode][10]) == 2:  # 노고돌
                                        if (고 <= float(input_high)):

                                            if time_cule == 0:
                                                self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                                if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                    self.savedstockitem.item_view[self.scode][14] = 1
                                                    print(self.scode + "노고돌")
                                                else:
                                                    self.savedstockitem.item_view[self.scode][14] = 0
                                                    print(self.scode + "노고돌")


                                            elif time_cule == input_time:
                                                self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                                if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                    self.savedstockitem.item_view[self.scode][14] = 1
                                                    print(self.scode + "노고돌")
                                                else:
                                                    self.savedstockitem.item_view[self.scode][14] = 0
                                                    print(self.scode + "노고돌")



                                    elif ((int(self.savedstockitem.item_view[self.scode][8]) == 1) and
                                          (int(self.savedstockitem.item_view[self.scode][9]) == 1) and
                                          (int(self.savedstockitem.item_view[self.scode][10]) == 1)):

                                        if time_cule == 0:
                                            # 거노고돌,거고돌,노고돌,아님
                                            self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                            if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                self.savedstockitem.item_view[self.scode][14] = 1
                                                print(self.scode + "거노고돌,거고돌,노고돌,아님")
                                            else:
                                                self.savedstockitem.item_view[self.scode][14] = 0
                                                print(self.scode + "거노고돌,거고돌,노고돌,아님")


                                        elif time_cule == input_time:
                                            # 거노고돌,거고돌,노고돌,아님
                                            self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                            if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                self.savedstockitem.item_view[self.scode][14] = 1
                                                print(self.scode + "거노고돌,거고돌,노고돌,아님")
                                            else:
                                                self.savedstockitem.item_view[self.scode][14] = 0
                                                print(self.scode + "거노고돌,거고돌,노고돌,아님")


                                else:  # 시가조건2
                                    print(self.scode + "#시가조건2")
                                    # self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                    # self.savedstockitem.item_view[self.scode][14] = 0

                        else:  # 매수비율조건 2

                            if (매수비율가 >= self.price):  # 매수비율가 비교
                                if int(self.savedstockitem.item_view[self.scode][7]) >= 2:  # 시가조건

                                    if int(self.savedstockitem.item_view[self.scode][9]) == 2:  # 거고돌
                                        if (고 > float(input_high)):
                                            if (고돌거래량 >= 1):

                                                if time_cule == 0:
                                                    self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code,
                                                                                        mesu,sss,sssddd)
                                                    if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                        self.savedstockitem.item_view[self.scode][14] = 1
                                                        print(self.scode + "비거고돌")
                                                    else:
                                                        self.savedstockitem.item_view[self.scode][14] = 0
                                                        print(self.scode + "비거고돌")


                                                elif time_cule == input_time:
                                                    self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code,
                                                                                        mesu,sss,sssddd)
                                                    if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                        self.savedstockitem.item_view[self.scode][14] = 1
                                                        print(self.scode + "비거고돌")
                                                    else:
                                                        self.savedstockitem.item_view[self.scode][14] = 0
                                                        print(self.scode + "비거고돌")




                                    elif int(self.savedstockitem.item_view[self.scode][8]) == 2:  # 거노고돌
                                        if (고 > float(input_high)):
                                            if current_time >= market_start_time:
                                                if (고돌거래량 < 1):

                                                    if time_cule == 0:
                                                        self.order_stock.CSPAT00600_request(self.scode,
                                                                                            qunti_stock_code, mesu,sss,sssddd)
                                                        if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                            self.savedstockitem.item_view[self.scode][14] = 1
                                                            print(self.scode + "비거노고돌")
                                                        else:
                                                            self.savedstockitem.item_view[self.scode][14] = 0
                                                            print(self.scode + "비거노고돌")


                                                    elif time_cule == input_time:
                                                        self.order_stock.CSPAT00600_request(self.scode,
                                                                                            qunti_stock_code, mesu,sss,sssddd)
                                                        if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                            self.savedstockitem.item_view[self.scode][14] = 1
                                                            print(self.scode + "비거노고돌")
                                                        else:
                                                            self.savedstockitem.item_view[self.scode][14] = 0
                                                            print(self.scode + "비거노고돌")




                                    elif int(self.savedstockitem.item_view[self.scode][10]) == 2:  # 노고돌
                                        if (고 <= float(input_high)):

                                            if time_cule == 0:
                                                self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                                if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                    self.savedstockitem.item_view[self.scode][14] = 1
                                                    print(self.scode + "비노고돌")
                                                else:
                                                    self.savedstockitem.item_view[self.scode][14] = 0
                                                    print(self.scode + "비노고돌")


                                            elif time_cule == input_time:
                                                self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                                if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                    self.savedstockitem.item_view[self.scode][14] = 1
                                                    print(self.scode + "비노고돌")
                                                else:
                                                    self.savedstockitem.item_view[self.scode][14] = 0
                                                    print(self.scode + "비노고돌")



                                    elif ((int(self.savedstockitem.item_view[self.scode][8]) == 1) and
                                          (int(self.savedstockitem.item_view[self.scode][9]) == 1) and
                                          (int(self.savedstockitem.item_view[self.scode][10]) == 1)):  # 거노고돌,거고돌,노고돌,아님

                                        if time_cule == 0:
                                            self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                            if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                self.savedstockitem.item_view[self.scode][14] = 1
                                                print(self.scode + "비거노고돌,비거고돌,비노고돌,아님")
                                            else:
                                                self.savedstockitem.item_view[self.scode][14] = 0
                                                print(self.scode + "비거노고돌,비거고돌,비노고돌,아님")


                                        elif time_cule == input_time:
                                            self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                            if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                self.savedstockitem.item_view[self.scode][14] = 1
                                                print(self.scode + "비거노고돌,비거고돌,비노고돌,아님")
                                            else:
                                                self.savedstockitem.item_view[self.scode][14] = 0
                                                print(self.scode + "비거노고돌,비거고돌,비노고돌,아님")



                                else:  # 시가조건2
                                    print(self.scode + "#시가조건2")
                                    # self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                    # self.savedstockitem.item_view[self.scode][14] = 0


                    else: ##plus buy

                        if int(self.savedstockitem.item_view[self.scode][14]) == 0:

                            if int(self.savedstockitem.item_view[self.scode][25]) == 1:
                                # print(mesuprice_stock_code2)
                                # print(type(mesuprice_stock_code2))

                                mesuprice_stock_code2 = 매수비율가 - (폭 * 1.25)

                                if (float(mesuprice_stock_code2) >= self.price):
                                    self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code,
                                                                        mesu,sss,sssddd)
                                    self.savedstockitem.item_view[self.scode][14] = 1


        # self.savedstockitem.item_jango[self.scode][2] = self.price_up_down

        self.sig_cl.signal_()


        ## 조건확인 코드 - 코스피와 동일하게 ##


        ## 조건확인 코드 - 코스피와 동일하게 ##
        """
        if int(self.volume) > 10 or int(self.volume) < -10: # 10주 초과하는 거래량만 수신받겠다.
            if self.scode in self.savedstockitem.item_saved:  # 처음 종목 등록이 아니라면 추가
                self.savedstockitem.item_saved[self.scode].append([self.scode, self.time, self.price, self.price_up_down, self.volume])
            else: # 처음 등록이라면
                self.savedstockitem.item_saved[self.scode] = [[self.scode, self.time, self.price, self.price_up_down, self.volume]]
        """

        """
        stockcode = self.GetFieldData("OutBlock", "shcode")
        price = self.GetFieldData("OutBlock", "price")
        chetime = self.GetFieldData("OutBlock", "chetime")
        print(self.count, stockcode, price, chetime)
        print(".... 실시간 TR code => {0}".format(tr_code))


    def _receive_real_data(self, tr_code):

        if tr_code == "S3_":
            self.scode = int(self.GetFieldData("OutBlock", "shcode"))
            self.time = int(self.GetFieldData("OutBlock", "chetime"))
            self.price = int(self.GetFieldData("OutBlock", "price"))
            if self.price < 0:
                self.price = self.price * (-1)
            self.price_up_down = self.GetFieldData("OutBlock", "drate")
            self.volume = int(self.GetFieldData("OutBlock", "volume"))
            self.hour = self.time / 10000
            self.min = self.time / 100 % 100
            self.sec = self.time % 100
            self.chcode = self.XQuery_t1101.request(self.scode)
        self.savedstockitem.item_view[self.scode] = [self.chcode, str(self.price), self.price_up_down]
        self.sig_cl.signal_()

        if self.volume > 10 or self.volume < -10:  # 10주 초과하는 거래량만 수신받겠다.
            if self.scode in self.savedstockitem.item_saved:  # 처음 종목 등록이 아니라면 추가
                self.savedstockitem.item_saved[self.scode].append(
                    [self.scode, self.time, self.price, self.price_up_down, self.volume])
            else:  # 처음 등록이라면
                self.savedstockitem.item_saved[self.scode] = [
                    [self.scode, self.time, self.price, self.price_up_down, self.volume]]
        """


    def start(self,tcode):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\S3_.res"  # RES 파일 등록
        self.SetFieldData("InBlock", "shcode", tcode)
        self.AdviseRealData()

        # 실시간데이터 요청


    def add_item(self, stockcode):
        # 실시간데이터 요청 종목 추가
        self.SetFieldData("InBlock", "shcode", stockcode)
        self.AdviseRealData()

    def remove_item(self, stockcode):
        # stockcode 종목만 실시간데이터 요청 취소
        self.UnadviseRealDataWithKey(stockcode)

    def end(self):
        self.UnadviseRealData()  # 실시간데이터 요청 모두 취소

    @classmethod
    def get_instance(cls):
        xreal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", cls)
        return xreal


class XReal_K3__(QAxWidget, QThread):

    def __init__(self):
        super().__init__()
        self.count = 0
        self.sig_cl = Sig_cl()
        self.savedstockitem = Savedstockitem()
        self.order_stock = order_stock()


    def OnReceiveRealData(self, tr_code):  # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count = 1

        if tr_code == "K3_":
            self.scode = str(self.GetFieldData("OutBlock", "shcode"))
            self.time = self.GetFieldData("OutBlock", "chetime")
            self.price = int(self.GetFieldData("OutBlock", "price"))
            self.open = int(self.GetFieldData("OutBlock", "open"))
            self.high = int(self.GetFieldData("OutBlock", "high"))
            if self.price < 0:
                self.price = self.price * (-1)
            self.price_up_down = self.GetFieldData("OutBlock", "drate")
            self.volume = self.GetFieldData("OutBlock", "cvolume")
            self.hour = int(self.time) / 10000
            self.min = int(self.time) / 100 % 100
            self.sec = int(self.time) % 100
            self.csode = self.scode
            # self.scode = "A" + self.scode  # 모의투자 self.scode

            if self.scode in self.savedstockitem.item_jango.keys():
                self.savedstockitem.item_jango[self.scode][2] = str(self.price)
                self.savedstockitem.item_jango[self.scode][16] = str(self.open)

                sc = self.savedstockitem.item_jango[self.scode][9] # 수동익절가
                asc = self.savedstockitem.item_jango[self.scode][7] # 자동익절가
                fsc = float(sc)
                fasc = float(asc)
                sl = self.savedstockitem.item_jango[self.scode][10] # 수동손절가
                asl = self.savedstockitem.item_jango[self.scode][8] # 자동손절가
                fsl = float(sl)
                fasl = float(asl)
                l = self.savedstockitem.item_jango[self.scode][15] # 최저점

                quanti = self.savedstockitem.item_jango[self.scode][4] # 수량
                medo = 1
                try:
                    if int(self.savedstockitem.item_jango[self.scode][6]) != 0:
                        sss = 101
                        sssddd = self.savedstockitem.item_jango[self.scode][6]

                    else:
                        sss = "000"
                        sssddd = ""
                except:
                    pass



                try:
                    if int(self.savedstockitem.item_view[self.scode][14]) == 0:
                        self.savedstockitem.item_jango[self.scode][11] = 99
                        self.savedstockitem.item_jango[self.scode][12] = 2
                        self.savedstockitem.item_jango[self.scode][13] = 2

                    else:
                        self.savedstockitem.item_jango[self.scode][11] = 99
                        self.savedstockitem.item_jango[self.scode][12] = 1
                        self.savedstockitem.item_jango[self.scode][13] = 1
                except:
                    pass

                if self.savedstockitem.item_check["감시"] == 1:
                    if int(self.savedstockitem.item_jango[self.scode][14]) == 2:
                        if int(self.savedstockitem.item_jango[self.scode][12]) == 2:  # 익절선택-2자동
                            if (fasc <= self.price):  # 현재가 조건
                                self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                self.savedstockitem.item_jango[self.scode][14] = 0
                                print(self.scode + "익절선택-2자동")

                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 2:  # 손절선택-2자동
                                if (fasl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-2자동")

                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 1:  # 손절선택-1수동
                                if (fsl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-1수동")

                        elif int(self.savedstockitem.item_jango[self.scode][12]) == 1:  # 익절선택-1수동
                            if (fsc <= self.price):  # 현재가 조건
                                self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                self.savedstockitem.item_jango[self.scode][14] = 0
                                print(self.scode + "익절선택-1수동")
                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 2:  # 손절선택-2자동
                                if (fasl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-2자동")

                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 1:  # 손절선택-1수동
                                if (fsl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-1수동")

                        elif int(self.savedstockitem.item_jango[self.scode][12]) == 0:  # 익절선택-0퍼센트
                            p = self.savedstockitem.item_jango[self.scode][11]  # 프로익절가
                            ll = float(l) / 100 * (100 + float(p))
                            fll = int(round(float(ll)))

                            print(fll)



                            if (fll <= self.price):  # 현재가 조건
                                self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                self.order_stock.CSPAT00600_request(self.scode, quanti, medo, sss, sssddd)
                                self.savedstockitem.item_jango[self.scode][14] = 0
                                print(self.scode + "익절선택-0퍼센트")

                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 2:  # 손절선택-2자동
                                if (fasl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-2자동")

                            elif int(self.savedstockitem.item_jango[self.scode][13]) == 1:  # 손절선택-1수동
                                if (fsl > self.price):  # 현재가 조건
                                    self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                                    self.savedstockitem.item_jango[self.scode][14] = 0
                                    print(self.scode + "손절선택-1수동")



                    # if (fsc <= self.price) or (fasc <= self.price) or (fsl > self.price) or (fasl > self.price):
                    #     self.order_stock.CSPAT00600_request(self.scode, quanti, medo,sss,sssddd)
                    #     print("매도 감시")

            if self.scode in self.savedstockitem.item_view.keys():

                self.savedstockitem.item_view[self.scode][2] = str(self.price)
                self.savedstockitem.item_view[self.scode][4] = str(self.high)
                self.savedstockitem.item_view[self.scode][3] = str(self.open)

                input_high = self.savedstockitem.item_view[self.scode][5]
                open_stock_code = self.savedstockitem.item_view[self.scode][7]
                volume_stock_code = self.savedstockitem.item_view[self.scode][8]
                high_stock_code = self.savedstockitem.item_view[self.scode][9]
                mesuprice_stock_code = self.savedstockitem.item_view[self.scode][12]
                qunti_stock_code = self.savedstockitem.item_view[self.scode][11]
                mesurate_stock_code = self.savedstockitem.item_view[self.scode][13]
                sinyung_stock_code = self.savedstockitem.item_view[self.scode][10]
                # result_stock_code = self.savedstockitem.item_view[self.scode][14]
                mesu = 2
                저 = float(self.savedstockitem.item_view[self.scode][26])
                고 = float(self.savedstockitem.item_view[self.scode][16])
                반등저점 = float(self.savedstockitem.item_view[self.scode][17])
                고돌거래량 = float(self.savedstockitem.item_view[self.scode][18])
                # 고돌 = float(self.savedstockitem.item_view[self.scode][19])
                매수비율가 = float(((1 - (float(mesurate_stock_code) / 1000)) * (고 - 저)) + 저)
                폭 = float(self.savedstockitem.item_view[self.scode][20])
                반등폭2 = 2 * 폭
                
                sss = "000"
                sssddd = ""
                
                # 15 - 저, 16 - 고, 17 - 반등저점, 18 - 고돌거래량, 19 - 고돌, 20 - 매수비율가
                try:
                    if int(self.savedstockitem.item_view[self.scode][3]) < int(
                            self.savedstockitem.item_view[self.scode][7]):

                        갭하락 = int(self.savedstockitem.item_view[self.scode][7]) - int(
                            self.savedstockitem.item_view[self.scode][3])
                        if int(갭하락) > 반등폭2:
                            mesuprice_stock_code = float(mesuprice_stock_code) - 반등폭2
                            매수비율가 = 매수비율가 - 반등폭2
                except:
                    pass






                ooppen_time = QTime(9, 0, 0)
                market_start_time = QTime(9, 15, 0)
                open_time = QTime(10, 30, 0)
                middle_time = QTime(14, 0, 0)
                time_cule = int(self.savedstockitem.item_view[self.scode][23])
                current_time = QTime.currentTime()
                input_time = int(self.savedstockitem.item_view[self.scode][22])
                if float(mesuprice_stock_code) > 0:
                    input_price = float(mesuprice_stock_code)
                else:
                    input_price = 매수비율가
                  # 입력 매수가
                # lowest_price = 저
                # print(input_time)
                if input_time != 0:
                    print("input_time1")
                    if current_time <= open_time:
                        print("input_time11")
                        if 반등저점 > input_price:
                            self.savedstockitem.item_view[self.scode][23] = 1
                            time_cule = self.savedstockitem.item_view[self.scode][23]
                        else:
                            self.savedstockitem.item_view[self.scode][23] = 1
                            time_cule = self.savedstockitem.item_view[self.scode][23]
                            self.savedstockitem.item_view[self.scode][22] = 4

                    elif current_time < middle_time:
                        print("input_time111")
                        if current_time > open_time:

                            if 반등저점 > input_price:
                                self.savedstockitem.item_view[self.scode][23] = 2
                                time_cule = self.savedstockitem.item_view[self.scode][23]
                            else:
                                self.savedstockitem.item_view[self.scode][23] = 2
                                time_cule = self.savedstockitem.item_view[self.scode][23]
                                self.savedstockitem.item_view[self.scode][22] = 4


                    elif current_time >= middle_time:
                        print("input_time2")
                        if 반등저점 > input_price:
                            self.savedstockitem.item_view[self.scode][23] = 3
                            time_cule = self.savedstockitem.item_view[self.scode][23]
                            print("input_time3")
                        else:
                            print("input_time4")
                            self.savedstockitem.item_view[self.scode][23] = 3
                            time_cule = self.savedstockitem.item_view[self.scode][23]
                            self.savedstockitem.item_view[self.scode][22] = 4

                input_time = int(self.savedstockitem.item_view[self.scode][22])

                try:
                    if current_time >= ooppen_time:

                        if int(self.savedstockitem.item_view[self.scode][3]) < int(
                                self.savedstockitem.item_view[self.scode][7]):

                            print(self.savedstockitem.item_view[self.scode][3])
                            print(self.savedstockitem.item_view[self.scode][7])

                            if int(self.savedstockitem.item_view[self.scode][24]) == 1:  # 갭상승 매수하고 싶으면 1
                                self.savedstockitem.item_view[self.scode][14] = 0

                        if int(self.savedstockitem.item_view[self.scode][3]) >= int(
                                self.savedstockitem.item_view[self.scode][7]):

                            if int(self.savedstockitem.item_view[self.scode][24]) == 2:  # 갭하락 매수하고 싶으면 2
                                self.savedstockitem.item_view[self.scode][14] = 0
                except:
                    pass

                self.savedstockitem.item_view[self.scode][15] = 매수비율가
                #print(self.savedstockitem.item_view[self.scode][26])

                bill_input = float(self.savedstockitem.item_view[self.scode][27])  # 입력한 글자 불러오는 메서드 text()

                mesu_input = float(매수비율가)

                # a = self.lineEdit.text()
                # print(self.savedstockitem.item_jango[self.scode][8])
                losep = (1 - (float(mesu_input) - (float(self.savedstockitem.item_view[self.scode][20]) * 2.3)) / float(
                    mesu_input)) * 100

                # now_num = self.savedstockitem.item_view[scode][2]

                # qunti = round(float(bill_input)/float(now_num))

                qunti_stock_code = round(float(bill_input) / float(mesu_input) / ((float(losep) / 100)))

                # 손절금 / 매수가 / (2 * (손절퍼센트 / 100))

                self.savedstockitem.item_view[self.scode][11] = qunti_stock_code

                print(self.savedstockitem.item_view[self.scode][11])

                if self.savedstockitem.item_check["감시"] == 1:  # 감지조건


                    if int(self.savedstockitem.item_view[self.scode][14]) >= 2:  # 종목별 감시결과조건

                        if int(self.savedstockitem.item_view[self.scode][13]) == 0:  # 매수비율조건

                            if (float(mesuprice_stock_code) >= self.price):  # 현재가 조건
                                if int(self.savedstockitem.item_view[self.scode][7]) >= 2:  # 전일종가 조건
                                    if int(self.savedstockitem.item_view[self.scode][9]) == 2:  # 거고돌
                                        if (고 > float(input_high)):
                                            if (고돌거래량 >= 1):
                                                if time_cule == 0:
                                                    self.order_stock.CSPAT00600_request(self.scode,
                                                                                        qunti_stock_code,
                                                                                        mesu,sss,sssddd)
                                                    if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                        self.savedstockitem.item_view[self.scode][14] = 1
                                                        print(self.scode + "거고돌")
                                                    else:
                                                        self.savedstockitem.item_view[self.scode][14] = 0
                                                        print(self.scode + "거고돌")


                                                elif time_cule == input_time:
                                                    self.order_stock.CSPAT00600_request(self.scode,
                                                                                        qunti_stock_code,
                                                                                        mesu,sss,sssddd)
                                                    if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                        self.savedstockitem.item_view[self.scode][14] = 1
                                                        print(self.scode + "거고돌")
                                                    else:
                                                        self.savedstockitem.item_view[self.scode][14] = 0
                                                        print(self.scode + "거고돌")




                                    elif int(self.savedstockitem.item_view[self.scode][8]) == 2:  # 거노고돌
                                        if (고 > float(input_high)):
                                            if current_time >= market_start_time:
                                                if (고돌거래량 < 1):

                                                    if time_cule == 0:
                                                        self.order_stock.CSPAT00600_request(self.scode,
                                                                                            qunti_stock_code, mesu,sss,sssddd)
                                                        if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                            self.savedstockitem.item_view[self.scode][14] = 1
                                                            print(self.scode + "거노고돌")
                                                        else:
                                                            self.savedstockitem.item_view[self.scode][14] = 0
                                                            print(self.scode + "거노고돌")



                                                    elif time_cule == input_time:
                                                        self.order_stock.CSPAT00600_request(self.scode,
                                                                                            qunti_stock_code, mesu,sss,sssddd)
                                                        if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                            self.savedstockitem.item_view[self.scode][14] = 1
                                                            print(self.scode + "거노고돌")
                                                        else:
                                                            self.savedstockitem.item_view[self.scode][14] = 0
                                                            print(self.scode + "거노고돌")




                                    elif int(self.savedstockitem.item_view[self.scode][10]) == 2:  # 노고돌
                                        if (고 <= float(input_high)):

                                            if time_cule == 0:
                                                self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code,
                                                                                    mesu,sss,sssddd)
                                                if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                    self.savedstockitem.item_view[self.scode][14] = 1
                                                    print(self.scode + "노고돌")
                                                else:
                                                    self.savedstockitem.item_view[self.scode][14] = 0
                                                    print(self.scode + "노고돌")


                                            elif time_cule == input_time:
                                                self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code,
                                                                                    mesu,sss,sssddd)
                                                if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                    self.savedstockitem.item_view[self.scode][14] = 1
                                                    print(self.scode + "노고돌")
                                                else:
                                                    self.savedstockitem.item_view[self.scode][14] = 0
                                                    print(self.scode + "노고돌")



                                    elif ((int(self.savedstockitem.item_view[self.scode][8]) == 1) and
                                          (int(self.savedstockitem.item_view[self.scode][9]) == 1) and
                                          (int(self.savedstockitem.item_view[self.scode][10]) == 1)):

                                        if time_cule == 0:
                                            # 거노고돌,거고돌,노고돌,아님
                                            self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                            if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                self.savedstockitem.item_view[self.scode][14] = 1
                                                print(self.scode + "거노고돌,거고돌,노고돌,아님")
                                            else:
                                                self.savedstockitem.item_view[self.scode][14] = 0
                                                print(self.scode + "거노고돌,거고돌,노고돌,아님")


                                        elif time_cule == input_time:
                                            # 거노고돌,거고돌,노고돌,아님
                                            self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                            if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                self.savedstockitem.item_view[self.scode][14] = 1
                                                print(self.scode + "거노고돌,거고돌,노고돌,아님")
                                            else:
                                                self.savedstockitem.item_view[self.scode][14] = 0
                                                print(self.scode + "거노고돌,거고돌,노고돌,아님")


                                else:  # 시가조건2
                                    print(self.scode + "#시가조건2")
                                    # self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                    # self.savedstockitem.item_view[self.scode][14] = 0

                        else:  # 매수비율조건 2

                            if (매수비율가 >= self.price):  # 매수비율가 비교
                                if int(self.savedstockitem.item_view[self.scode][7]) >= 2:  # 시가조건

                                    if int(self.savedstockitem.item_view[self.scode][9]) == 2:  # 거고돌
                                        if (고 > float(input_high)):
                                            if (고돌거래량 >= 1):

                                                if time_cule == 0:
                                                    self.order_stock.CSPAT00600_request(self.scode,
                                                                                        qunti_stock_code,
                                                                                        mesu,sss,sssddd)
                                                    if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                        self.savedstockitem.item_view[self.scode][14] = 1
                                                        print(self.scode + "비거고돌")
                                                    else:
                                                        self.savedstockitem.item_view[self.scode][14] = 0
                                                        print(self.scode + "비거고돌")


                                                elif time_cule == input_time:
                                                    self.order_stock.CSPAT00600_request(self.scode,
                                                                                        qunti_stock_code,
                                                                                        mesu,sss,sssddd)
                                                    if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                        self.savedstockitem.item_view[self.scode][14] = 1
                                                        print(self.scode + "비거고돌")
                                                    else:
                                                        self.savedstockitem.item_view[self.scode][14] = 0
                                                        print(self.scode + "비거고돌")




                                    elif int(self.savedstockitem.item_view[self.scode][8]) == 2:  # 거노고돌
                                        if (고 > float(input_high)):
                                            if current_time >= market_start_time:
                                                if (고돌거래량 < 1):

                                                    if time_cule == 0:
                                                        self.order_stock.CSPAT00600_request(self.scode,
                                                                                            qunti_stock_code, mesu,sss,sssddd)
                                                        if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                            self.savedstockitem.item_view[self.scode][14] = 1
                                                            print(self.scode + "비거노고돌")
                                                        else:
                                                            self.savedstockitem.item_view[self.scode][14] = 0
                                                            print(self.scode + "비거노고돌")


                                                    elif time_cule == input_time:
                                                        self.order_stock.CSPAT00600_request(self.scode,
                                                                                            qunti_stock_code, mesu,sss,sssddd)
                                                        if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                            self.savedstockitem.item_view[self.scode][14] = 1
                                                            print(self.scode + "비거노고돌")
                                                        else:
                                                            self.savedstockitem.item_view[self.scode][14] = 0
                                                            print(self.scode + "비거노고돌")




                                    elif int(self.savedstockitem.item_view[self.scode][10]) == 2:  # 노고돌
                                        if (고 <= float(input_high)):

                                            if time_cule == 0:
                                                self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code,
                                                                                    mesu,sss,sssddd)
                                                if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                    self.savedstockitem.item_view[self.scode][14] = 1
                                                    print(self.scode + "비노고돌")
                                                else:
                                                    self.savedstockitem.item_view[self.scode][14] = 0
                                                    print(self.scode + "비노고돌")


                                            elif time_cule == input_time:
                                                self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code,
                                                                                    mesu,sss,sssddd)
                                                if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                    self.savedstockitem.item_view[self.scode][14] = 1
                                                    print(self.scode + "비노고돌")
                                                else:
                                                    self.savedstockitem.item_view[self.scode][14] = 0
                                                    print(self.scode + "비노고돌")



                                    elif ((int(self.savedstockitem.item_view[self.scode][8]) == 1) and
                                          (int(self.savedstockitem.item_view[self.scode][9]) == 1) and
                                          (int(self.savedstockitem.item_view[self.scode][
                                                   10]) == 1)):  # 거노고돌,거고돌,노고돌,아님

                                        if time_cule == 0:
                                            print(time_cule)
                                            print("time_0")
                                            print(반등저점)
                                            print(current_time)
                                            print(middle_time)
                                            print(input_time)
                                            print(int(self.savedstockitem.item_view[self.scode][22]))
                                            self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                            if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                self.savedstockitem.item_view[self.scode][14] = 1
                                                print(self.scode + "비거노고돌,비거고돌,비노고돌,아님")
                                            else:
                                                self.savedstockitem.item_view[self.scode][14] = 0
                                                print(self.scode + "비거노고돌,비거고돌,비노고돌,아님")


                                        elif time_cule == input_time:
                                            print(time_cule)
                                            print(input_time)
                                            self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                            if int(self.savedstockitem.item_view[self.scode][14]) == 3:
                                                self.savedstockitem.item_view[self.scode][14] = 1
                                                print(self.scode + "비거노고돌,비거고돌,비노고돌,아님")
                                            else:
                                                self.savedstockitem.item_view[self.scode][14] = 0
                                                print(self.scode + "비거노고돌,비거고돌,비노고돌,아님")



                                else:  # 시가조건2
                                    print(self.scode + "#시가조건2")
                                    # self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code, mesu,sss,sssddd)
                                    # self.savedstockitem.item_view[self.scode][14] = 0

                    else: ##plus buy

                        if int(self.savedstockitem.item_view[self.scode][14]) == 0:

                            if int(self.savedstockitem.item_view[self.scode][25]) == 1:
                                # print(mesuprice_stock_code2)
                                # print(type(mesuprice_stock_code2))

                                mesuprice_stock_code2 = 매수비율가 - (폭 * 1.25)

                                if (float(mesuprice_stock_code2) >= self.price):
                                    self.order_stock.CSPAT00600_request(self.scode, qunti_stock_code,
                                                                        mesu,sss,sssddd)
                                    self.savedstockitem.item_view[self.scode][14] = 1




            # self.savedstockitem.item_jango[self.scode][2] = self.price_up_down

        self.sig_cl.signal_()
        ## 조건확인 코드 - 코스피와 동일하게 ##


        ## 조건확인 코드 - 코스피와 동일하게 ##

        """
        if int(self.volume) > 10 or int(self.volume) < -10: # 10주 초과하는 거래량만 수신받겠다.
            if self.scode in self.savedstockitem.item_saved:  # 처음 종목 등록이 아니라면 추가
                self.savedstockitem.item_saved[self.scode].append([self.scode, self.time, self.price, self.price_up_down, self.volume])
            else: # 처음 등록이라면
                self.savedstockitem.item_saved[self.scode] = [[self.scode, self.time, self.price, self.price_up_down, self.volume]]
        """

        """
        stockcode = self.GetFieldData("OutBlock", "shcode")
        price = self.GetFieldData("OutBlock", "price")
        chetime = self.GetFieldData("OutBlock", "chetime")
        print(self.count, stockcode, price, chetime)
        print(".... 실시간 TR code => {0}".format(tr_code))


    def _receive_real_data(self, tr_code):

        if tr_code == "S3_":
            self.scode = int(self.GetFieldData("OutBlock", "shcode"))
            self.time = int(self.GetFieldData("OutBlock", "chetime"))
            self.price = int(self.GetFieldData("OutBlock", "price"))
            if self.price < 0:
                self.price = self.price * (-1)
            self.price_up_down = self.GetFieldData("OutBlock", "drate")
            self.volume = int(self.GetFieldData("OutBlock", "volume"))
            self.hour = self.time / 10000
            self.min = self.time / 100 % 100
            self.sec = self.time % 100
            self.chcode = self.XQuery_t1101.request(self.scode)
        self.savedstockitem.item_view[self.scode] = [self.chcode, str(self.price), self.price_up_down]
        self.sig_cl.signal_()

        if self.volume > 10 or self.volume < -10:  # 10주 초과하는 거래량만 수신받겠다.
            if self.scode in self.savedstockitem.item_saved:  # 처음 종목 등록이 아니라면 추가
                self.savedstockitem.item_saved[self.scode].append(
                    [self.scode, self.time, self.price, self.price_up_down, self.volume])
            else:  # 처음 등록이라면
                self.savedstockitem.item_saved[self.scode] = [
                    [self.scode, self.time, self.price, self.price_up_down, self.volume]]
        """


    def start(self,tcode):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\K3_.res"  # RES 파일 등록
        self.SetFieldData("InBlock", "shcode", tcode)
        self.AdviseRealData()
        # 실시간데이터 요청

    def add_item(self, stockcode):
        # 실시간데이터 요청 종목 추가
        self.SetFieldData("InBlock", "shcode", stockcode)
        self.AdviseRealData()

    def remove_item(self, stockcode):
        # stockcode 종목만 실시간데이터 요청 취소
        self.UnadviseRealDataWithKey(stockcode)

    def end(self):
        self.UnadviseRealData()  # 실시간데이터 요청 모두 취소

    @classmethod
    def get_instance(cls):
        xreal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", cls)
        return xreal

    """"""


class order_stock(QAxWidget, QThread):
    def __init__(self):
        super().__init__()
        self.is_data_received = False
        self.sig_cl = Sig_cl()
        self.savedstockitem = Savedstockitem()
        self.t0424 = t0424.get_instance()

    def CSPAT00600_ReceiveData(self, code):
        print(code)
        self.is_data_received = True


    def CSPAT00600_ReceiveMessage(self, code):
        print(code)
        self.is_data_received = True
        # self.savedstockitem.item_jango[stock_code] = ['', '', '', '']


    def CSPAT00600_request(self, scode , quanti, gubun, sss, sssddd):
        print('주문요청')
        self.savedstockitem.Save()
        self.t0424.t0424_request()

        """
        이베스트 서버에 일회성 TR data 요청함.
        """
        """"""

        self.ActiveX = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        self.ActiveX.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CSPAT00600.res"
        # RES 파일 등록
        """
        self.SetFieldData("t0424InBlock", "accno", 0, "20431636501")
        self.SetFieldData("t0424InBlock", "passwd", 0, "2072")
        self.SetFieldData("t0424InBlock", "prcgb", 0, "1")
        self.SetFieldData("t0424InBlock", "chegb", 0, "2")
        self.SetFieldData("t0424InBlock", "dangb", 0, "0")
        self.SetFieldData("t0424InBlock", "charge", 0, "1")
        self.SetFieldData("t0424InBlock", "cts_expcode", 0, cts_expcode )
        2072


        
        self.SetFieldData("CSPAQ12300InBlock1", "RecCnt", 0, "00001")
        self.SetFieldData("CSPAQ12300InBlock1", "AcntNo", 0, "55500651101")
        self.SetFieldData("CSPAQ12300InBlock1", "Pwd", 0, "0000")
        self.SetFieldData("CSPAQ12300InBlock1", "BalCreTp", 0, "0")
        self.SetFieldData("CSPAQ12300InBlock1", "CmsnAppTpCode", 0, "0")
        self.SetFieldData("CSPAQ12300InBlock1", "D2balBaseQryTp", 0, "1")
        self.SetFieldData("CSPAQ12300InBlock1", "UprcTpCode", 0, "0")

        self.Request(False)
        
        """
        #매수 2 , 매도 1
        if gubun == 2:
            jumon = '03'
        elif gubun == 1:
            jumon = '03'



        self.ActiveX.SetFieldData("CSPAT00600InBlock1", "AcntNo", 0, "20431636501")
        self.ActiveX.SetFieldData("CSPAT00600InBlock1", "InptPwd", 0, "2072")
        self.ActiveX.SetFieldData("CSPAT00600InBlock1", "IsuNo", 0, scode)
        self.ActiveX.SetFieldData("CSPAT00600InBlock1", "OrdQty", 0, quanti)
        self.ActiveX.SetFieldData("CSPAT00600InBlock1", "OrdPrc", 0, 0)
        self.ActiveX.SetFieldData("CSPAT00600InBlock1", "BnsTpCode", 0, gubun)
        self.ActiveX.SetFieldData("CSPAT00600InBlock1", "OrdprcPtnCode", 0, jumon)
        self.ActiveX.SetFieldData("CSPAT00600InBlock1", "MgntrnCode", 0, sss)
        self.ActiveX.SetFieldData("CSPAT00600InBlock1", "LoanDt", 0, sssddd)
        self.ActiveX.SetFieldData("CSPAT00600InBlock1", "OrdCndiTpCode", 0, "0")

        self.ActiveX.Request(False)

        """
        print("CSPAT00600_request")
        while self.is_data_received == False:
            print("CSPAT00600_request")
            pythoncom.PumpWaitingMessages()
        """

    @classmethod
    def get_instance(cls):
        CSPAT00600 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return CSPAT00600


class XAQueryEvents(object):
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def OnReceiveMessage(self, systemError, messageCode, message):
        if self.parent != None:
            self.parent.OnReceiveMessage(systemError, messageCode, message)

    def OnReceiveData(self, szTrCode):
        if self.parent != None:
            self.parent.OnReceiveData(szTrCode)

    def OnReceiveChartRealData(self, szTrCode):
        if self.parent != None:
            self.parent.OnReceiveChartRealData(szTrCode)

    def OnReceiveSearchRealData(self, szTrCode):
        if self.parent != None:
            self.parent.OnReceiveSearchRealData(szTrCode)

"""
class Worker(QAxWidget):

    def __init__(self):
        super().__init__()
        self.running = True
        self.chartindex = chartindex.get_instance()

    def stat(self):
        threading.Timer(10, self.run).start()

    def run(self):
        print("되니2")
        while self.running:
            print("안녕하세요")
            self.chartindex.chartindex_request_all()

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False

    """
"""
class stockgridview(QThread, QWidget):

    def __init__(self):
        super().__init__()
        self.running = True

        self.xreal = XReal_S3__.get_instance()  # S3 인스턴스
        self.xreal_K3 = XReal_K3__.get_instance()  # K3 인스턴스
        self.t0424 = t0424.get_instance()  # 잔고 인스턴스
        self.t1102 = t1102.get_instance()  # 매수 종목 인스턴스

        self.savedstockitem = Savedstockitem()
        #self.stockgridview = stockgridview()

        self.xreal.sig_cl.sig_.connect(self.update) #메인창에 수신된 S3 실시간 데이터 출력
        self.xreal_K3.sig_cl.sig_.connect(self.update) #메인창에 수신된 K3 실시간 데이터 출력
        self.t0424.sig_cl.sig_.connect(self.update) #메인창에 수신된 잔고 데이터 출력
        self.t1102.sig_cl.sig_.connect(self.update)  # 메인창에 수신된 잔고 데이터 출력

        self.tableWidget = QTableWidget()



    def update(self):

        self.tableWidget.setRowCount(0)

        if len(self.savedstockitem.item_jango) != 0:
            self.tableWidget_2.setRowCount(0)

            item_cnt = len(self.savedstockitem.item_jango)

            scode_list = list(self.savedstockitem.item_jango.keys())

            self.tableWidget_2.setRowCount(item_cnt)


            for i in range(item_cnt):

                for j in range(15):

                    item = QTableWidgetItem(self.savedstockitem.item_jango[scode_list[i]][j])

                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)

                    # 표 속성 가운데 정렬
                    self.tableWidget_2.setItem(i, j, item)



        if len(self.savedstockitem.item_view) != 0:
            self.tableWidget.setRowCount(0)



            item_cnt_v = len(self.savedstockitem.item_view)



            scode_list_v = list(self.savedstockitem.item_view.keys())



            self.tableWidget.setRowCount(item_cnt_v)



            for i in range(item_cnt_v):

                for j in range(15):

                    item = QTableWidgetItem(self.savedstockitem.item_view[scode_list_v[i]][j])

                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)

                    # 표 속성 가운데 정렬
                    self.tableWidget.setItem(i, j, item)
    """
"""
"""
"""
if __name__ == "__main__":
    def get_single_data(tcode):
        xq_t1101 = XQuery_t1101.get_instance()
        xq_t1101.request(tcode)

        while xq_t1101.is_data_received == False:
            pythoncom.PumpWaitingMessages()


    def get_real_data(tcode):
        xreal = XReal_S3_.get_instance()
        xreal.start(tcode)

        while xreal.count < 100:
            pythoncom.PumpWaitingMessages()

            if xreal.count == 5:
                xreal.add_item("003490")  # 대한항공 실시간 조회 추가

            if xreal.count == 20:
                xreal.remove_item("005930")  # 삼성전자 실시간 조회 제거

            if xreal.count == 30:
                xreal.end()  # 실시간 조회 중단.
                time.sleep(10)
                print("---- end -----")
                break


    xsession = xing_login.XSession.get_instance()
    xsession.api_login()

    get_single_data("105840")
    get_real_data("105840")
            """
"""
class Kiwoom(QAxWidget): #키움 api를 사용
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self.sig_cl = Sig_cl()  # 시그널 객체 생성
        self.savedstockitem = Savedstockitem()

    def _create_kiwoom_instance(self):  #키움 api를 사용가능하게 하는 메서드
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def signal_kiwoom(self): #시그널 신호용 메서드
        self.sig_cl.signal_()

    def comm_connect(self): #로그인창 요청 메서드
        self.dynamicCall("CommConnect()")

    def get_master_code_name(self, code): #종목명 반환하는 메서드
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def setrealreg(self, scrnum, trcode, fid, realtype): #실시간 데이터 요청
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", scrnum, trcode, fid, realtype)

    def _receive_real_data(self, scode, realtype, realdata):
        if realtype == "주식체결":
            self.scode = scode
            self.time = int(self.GetCommRealData(scode, 20))
            self.price= int(self.GetCommRealData(scode, 10))
            if self.price < 0:
                self.price = self.price*(-1)
            self.price_up_down = self.GetCommRealData(scode, 12)
            self.volume = int(self.GetCommRealData(scode, 15))
            self.hour = self.time/10000
            self.min = self.time / 100 % 100
            self.sec = self.time % 100
            self.chcode = self.get_master_code_name(scode)
        self.savedstockitem.item_view[scode] = [self.chcode, str(self.price), self.price_up_down]
        self.sig_cl.signal_()

        if self.volume > 10 or self.volume < -10: # 10주 초과하는 거래량만 수신받겠다.
            if scode in self.savedstockitem.item_saved:  # 처음 종목 등록이 아니라면 추가
                self.savedstockitem.item_saved[scode].append([self.scode, self.time, self.price, self.price_up_down, self.volume])
            else: # 처음 등록이라면
                self.savedstockitem.item_saved[scode] = [[self.scode, self.time, self.price, self.price_up_down, self.volume]]

#################################################################################################
#################아래는 실시간 데이터 요청과는 무관한 tr 데이터 요청용 메서드 ###################

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def set_input_value(self, id, value): #tr데이터 요청
        self.dynamicCall("SetInputValue(QString, QString)", id, value)




   
    
"""