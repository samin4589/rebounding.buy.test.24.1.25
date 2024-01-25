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

import win32com.client
import pythoncom

import time

import xing_login


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
        else:
            self.login_state = 2
            print("로그인 fail.. \n code={0}, message={1}\n".format(code, msg))

    def api_login(self, id="soni4589", pwd="vcxz1245", cert_pwd="vcxz1245!!"): # id, 암호, 공인인증서 암호
        self.ConnectServer("hts.ebestsec.co.kr", 20001)
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
        print("종목;{0},현재가;{1}, 누적거래량;{2}".format(name, price, volume))
        print("TR code => {0}".format(tr_code))

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
        print("종목;{0},현재가;{1}, 누적거래량;{2}".format(name, price, volume))
        print("TR code => {0}".format(tr_code))

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


class XReal_S3_(QAxWidget, QThread):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.sig_cl = Sig_cl()
        self.savedstockitem = Savedstockitem()

    def OnReceiveRealData(self, tr_code):  # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count = 1

        if tr_code == "S3_":
            self.scode = str(self.GetFieldData("OutBlock", "shcode"))
            self.time = self.GetFieldData("OutBlock", "chetime")
            self.price = int(self.GetFieldData("OutBlock", "price"))
            if self.price < 0:
                self.price = self.price * (-1)
            self.price_up_down = self.GetFieldData("OutBlock", "drate")
            self.volume = self.GetFieldData("OutBlock", "cvolume")
            self.hour = int(self.time) / 10000
            self.min = int(self.time) / 100 % 100
            self.sec = int(self.time) % 100
            #self.chcode = self.XQuery_t1101.request(self.scode)
            self.savedstockitem.item_view[self.scode][0] = self.scode
            self.savedstockitem.item_view[self.scode][1] = str(self.price)
            self.savedstockitem.item_view[self.scode][2] = self.price_up_down

            print(self.savedstockitem.item_view)

            self.sig_cl.signal_()

        if tr_code == "S3_":
            self.scode = str(self.GetFieldData("OutBlock", "shcode"))
            self.time = self.GetFieldData("OutBlock", "chetime")
            self.price = int(self.GetFieldData("OutBlock", "price"))
            if self.price < 0:
                self.price = self.price * (-1)
            self.price_up_down = self.GetFieldData("OutBlock", "drate")
            self.volume = self.GetFieldData("OutBlock", "cvolume")
            self.hour = int(self.time) / 10000
            self.min = int(self.time) / 100 % 100
            self.sec = int(self.time) % 100
            #self.chcode = self.XQuery_t1101.request(self.scode)
            self.savedstockitem.item_view[self.scode][0] = self.scode
            self.savedstockitem.item_view[self.scode][1] = str(self.price)
            self.savedstockitem.item_view[self.scode][2] = self.price_up_down

            print(self.savedstockitem.item_view)

            self.sig_cl.signal_()


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
        self.AdviseRealData()   # 실시간데이터 요청


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
