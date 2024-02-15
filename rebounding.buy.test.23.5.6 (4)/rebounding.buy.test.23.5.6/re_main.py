import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Controller import *
from Savedstockitem import *
import pickle

from PyQt5.QtCore import QTime


from PyQt5.QtTest import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'C:/Users/admin/Downloads/rebounding.buy.test.23.5.6 (3)/rebounding.buy.test.23.5.6', relative_path)


form = resource_path('main_test_buy.12.6.ui')
form_class = uic.loadUiType(form)[0]
#form_class = uic.loadUiType("main_test_buy.12.1.ui")[0] #0


class chartindex(QThread):

    def __init__(self):
        super().__init__()
        self.is_data_received = False
        self.sig_cl = Sig_cl()
        self.t0424 = t0424.get_instance()
        self.savedstockitem = Savedstockitem()
        #self.chartindex = chartindex.get_instance()


    def OnReceiveData(self, code):

        try:

            if self.i in self.savedstockitem.item_jango.keys():

                self.nCount = self.GetBlockCount("ChartIndexOutBlock1")

                if self.savedstockitem.item_jango[self.i][16] == self.GetFieldData("ChartIndexOutBlock1", "value5",
                                                                                   self.nCount - 1).strip():
                    # 지표 1 - 저, 지표 2 - 고, 지표 3 - 반등저점, 지표 4 - 고돌거래량, 지표 5 - 고돌
                    저 = float(self.GetFieldData("ChartIndexOutBlock1", "value1", self.nCount - 1).strip())
                    고 = float(self.GetFieldData("ChartIndexOutBlock1", "value2", self.nCount - 1).strip())
                    반등저점 = float(self.GetFieldData("ChartIndexOutBlock1", "value3", self.nCount - 1).strip())
                    고돌거래량 = self.GetFieldData("ChartIndexOutBlock1", "value4", self.nCount - 1).strip()
                    당시가 = self.GetFieldData("ChartIndexOutBlock1", "value5", self.nCount - 1).strip()

                    반등폭 = float(고 - 저) * 0.618 - float(고 - 저) * 0.5

                    self.savedstockitem.item_jango[self.i][7] = str(
                        round(float(반등저점) + 1.8 * (float(고 - 저) * 0.618 - float(고 - 저) * 0.5)))

                    c = float(self.savedstockitem.item_jango[self.i][3]) - (float(반등폭) * 2.3)
                    self.savedstockitem.item_jango[self.i][8] = str(round(c))
                    self.savedstockitem.item_jango[self.i][15] = float(반등저점)
                    # self.savedstockitem.item_jango[self.i][16] = str(당시가)

        except:
            print("잔고조회안함")

        try:
            # 당시가 = float(self.GetFieldData("ChartIndexOutBlock1", "value5", self.nCount - 1).strip())

            if self.z in self.savedstockitem.item_view.keys():

                self.nCount = self.GetBlockCount("ChartIndexOutBlock1")
                # if 1==1:
                print(self.z)
                print(self.GetFieldData("ChartIndexOutBlock1", "value1", self.nCount - 1).strip())  # 저가v1
                print(type(self.GetFieldData("ChartIndexOutBlock1", "value5", self.nCount - 1).strip()))  # 시가v5
                if str(self.GetFieldData("ChartIndexOutBlock1", "value5", self.nCount - 1).strip()) != "":
                    print("공백")

                    if self.savedstockitem.item_view[self.z][3] == self.GetFieldData("ChartIndexOutBlock1", "value5",
                                                                                     self.nCount - 1).strip():
                        print("공백2")
                        저 = float(self.GetFieldData("ChartIndexOutBlock1", "value1", self.nCount - 1).strip())
                        고 = float(self.GetFieldData("ChartIndexOutBlock1", "value2", self.nCount - 1).strip())
                        반등저점 = float(self.GetFieldData("ChartIndexOutBlock1", "value3", self.nCount - 1).strip())
                        고돌거래량 = float(self.GetFieldData("ChartIndexOutBlock1", "value4", self.nCount - 1).strip())
                        당시가 = float(self.GetFieldData("ChartIndexOutBlock1", "value5", self.nCount - 1).strip())

                        반등폭 = float(고 - 저) * 0.618 - float(고 - 저) * 0.5

                        # self.savedstockitem.item_view[self.z][5] = str(round(당시가))
                        self.savedstockitem.item_view[self.z][26] = str(round(저))
                        self.savedstockitem.item_view[self.z][16] = str(round(고))
                        self.savedstockitem.item_view[self.z][17] = str(round(반등저점))
                        self.savedstockitem.item_view[self.z][18] = str(round(고돌거래량))
                        self.savedstockitem.item_view[self.z][20] = str(round(반등폭))
                        print('반등폭'+self.savedstockitem.item_view[self.z][20])
                    elif self.savedstockitem.item_view[self.z][21] == self.GetFieldData("ChartIndexOutBlock1", "value1",
                                                                                        self.nCount - 2).strip():
                        print("공백3")
                        저 = float(self.GetFieldData("ChartIndexOutBlock1", "value1", self.nCount - 2).strip())
                        고 = float(self.GetFieldData("ChartIndexOutBlock1", "value2", self.nCount - 2).strip())
                        반등저점 = float(self.GetFieldData("ChartIndexOutBlock1", "value3", self.nCount - 2).strip())
                        고돌거래량 = float(self.GetFieldData("ChartIndexOutBlock1", "value4", self.nCount - 2).strip())
                        당시가 = float(self.GetFieldData("ChartIndexOutBlock1", "value5", self.nCount - 2).strip())

                        반등폭 = float(고 - 저) * 0.618 - float(고 - 저) * 0.5

                        # self.savedstockitem.item_view[self.z][5] = str(round(당시가))
                        self.savedstockitem.item_view[self.z][26] = str(round(저))
                        self.savedstockitem.item_view[self.z][16] = str(round(고))
                        self.savedstockitem.item_view[self.z][17] = str(round(반등저점))
                        self.savedstockitem.item_view[self.z][18] = str(round(고돌거래량))
                        self.savedstockitem.item_view[self.z][20] = str(round(반등폭))


                elif int(self.savedstockitem.item_view[self.z][21]) > 0:
                    print("장최")
                    if self.savedstockitem.item_view[self.z][21] == self.GetFieldData("ChartIndexOutBlock1", "value1",
                                                                                      self.nCount - 2).strip():
                        저 = float(self.GetFieldData("ChartIndexOutBlock1", "value1", self.nCount - 2).strip())
                        고 = float(self.GetFieldData("ChartIndexOutBlock1", "value2", self.nCount - 2).strip())
                        반등저점 = float(self.GetFieldData("ChartIndexOutBlock1", "value3", self.nCount - 2).strip())
                        고돌거래량 = float(self.GetFieldData("ChartIndexOutBlock1", "value4", self.nCount - 2).strip())
                        당시가 = float(self.GetFieldData("ChartIndexOutBlock1", "value5", self.nCount - 2).strip())

                        반등폭 = float(고 - 저) * 0.618 - float(고 - 저) * 0.5

                        # self.savedstockitem.item_view[self.z][5] = str(round(당시가))
                        self.savedstockitem.item_view[self.z][26] = str(round(저))
                        self.savedstockitem.item_view[self.z][16] = str(round(고))
                        self.savedstockitem.item_view[self.z][17] = str(round(반등저점))
                        self.savedstockitem.item_view[self.z][18] = str(round(고돌거래량))
                        self.savedstockitem.item_view[self.z][20] = str(round(반등폭))


        except:
            print("매수부 조회안됨")

    def chartindex_request(self):

        """
        이베스트 서버에 일회성 TR data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\ChartIndex.res"
        # RES 파일 등록

        keylist = self.savedstockitem.item_jango.keys()

        for self.i in keylist:
            a = self.i
            # print("chart_request")
            # b = self.savedstockitem.item_jango[self.i][16]
            # print(b)
            # self.RemoveService("ChartIndex", "")
            # self.SetFieldData("ChartIndexInBlock", "indexid", 0, b)
            self.SetFieldData("ChartIndexInBlock", "indexname", 0, "피보나치매수매도1")
            self.SetFieldData("ChartIndexInBlock", "market", 0, "1")
            self.SetFieldData("ChartIndexInBlock", "period", 0, "1")
            self.SetFieldData("ChartIndexInBlock", "shcode", 0, a)
            self.SetFieldData("ChartIndexInBlock", "qrycnt", 0, "500")
            self.SetFieldData("ChartIndexInBlock", "ncnt", 0, "15")
            self.SetFieldData("ChartIndexInBlock", "sdate", 0, "")
            self.SetFieldData("ChartIndexInBlock", "edate", 0, "")
            self.SetFieldData("ChartIndexInBlock", "Isamend", 0, "0")
            self.SetFieldData("ChartIndexInBlock", "Isgab", 0, "0")
            self.SetFieldData("ChartIndexInBlock", "IsReal", 0, "0")

            self.RequestService("ChartIndex", "")
            # time.sleep(2)
            QTest.qWait(2400)

        # print(a)
        """
        while self.is_data_received == False:
            print("chart_request00")
            pythoncom.PumpWaitingMessages()
        """

    def chartindex_request_mesu(self,m):

        """
        이베스트 서버에 일회성 TR data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\ChartIndex.res"
        # RES 파일 등록

        keylist = self.savedstockitem.item_view.keys()

        #for self.z in keylist:
        self.z = m
        # print("chart_request")

        # self.RemoveService("ChartIndex", "")

        self.SetFieldData("ChartIndexInBlock", "indexname", 0, "피보나치매수매도1")
        self.SetFieldData("ChartIndexInBlock", "market", 0, "1")
        self.SetFieldData("ChartIndexInBlock", "period", 0, "1")
        self.SetFieldData("ChartIndexInBlock", "shcode", 0, self.z)
        self.SetFieldData("ChartIndexInBlock", "qrycnt", 0, "500")
        self.SetFieldData("ChartIndexInBlock", "ncnt", 0, "15")
        self.SetFieldData("ChartIndexInBlock", "sdate", 0, "")
        self.SetFieldData("ChartIndexInBlock", "edate", 0, "")
        self.SetFieldData("ChartIndexInBlock", "Isamend", 0, "0")
        self.SetFieldData("ChartIndexInBlock", "Isgab", 0, "0")
        self.SetFieldData("ChartIndexInBlock", "IsReal", 0, "0")

        self.RequestService("ChartIndex", "")
        # time.sleep(2)
        #QTest.qWait(1200)

        # print(a)
        """
        while self.is_data_received == False:
            print("chart_request00")
            pythoncom.PumpWaitingMessages()
        """

    def chartindex_request_all(self):

        """
        이베스트 서버에 일회성 TR data 요청함.
        """

        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\ChartIndex.res"
        # RES 파일 등록

        keylist = self.savedstockitem.item_view.keys()
        print("dkehl")

        for self.z in keylist:

            a = self.z
            # print("chart_request")

            # self.RemoveService("ChartIndex", "")
            print("dkehl")
            self.SetFieldData("ChartIndexInBlock", "indexname", 0, "피보나치매수매도1")
            self.SetFieldData("ChartIndexInBlock", "market", 0, "1")
            self.SetFieldData("ChartIndexInBlock", "period", 0, "1")
            self.SetFieldData("ChartIndexInBlock", "shcode", 0, a)
            self.SetFieldData("ChartIndexInBlock", "qrycnt", 0, "500")
            self.SetFieldData("ChartIndexInBlock", "ncnt", 0, "15")
            self.SetFieldData("ChartIndexInBlock", "sdate", 0, "")
            self.SetFieldData("ChartIndexInBlock", "edate", 0, "")
            self.SetFieldData("ChartIndexInBlock", "Isamend", 0, "0")
            self.SetFieldData("ChartIndexInBlock", "Isgab", 0, "0")
            self.SetFieldData("ChartIndexInBlock", "IsReal", 0, "0")
            print("dkehl")
            self.RequestService("ChartIndex", "")
            # time.sleep(2)
            QTest.qWait(2400)

        keylist = self.savedstockitem.item_jango.keys()

        for self.i in keylist:
            a = self.i
            # print("chart_request")

            # self.RemoveService("ChartIndex", "")

            self.SetFieldData("ChartIndexInBlock", "indexname", 0, "피보나치매수매도1")
            self.SetFieldData("ChartIndexInBlock", "market", 0, "1")
            self.SetFieldData("ChartIndexInBlock", "period", 0, "1")
            self.SetFieldData("ChartIndexInBlock", "shcode", 0, a)
            self.SetFieldData("ChartIndexInBlock", "qrycnt", 0, "500")
            self.SetFieldData("ChartIndexInBlock", "ncnt", 0, "15")
            self.SetFieldData("ChartIndexInBlock", "sdate", 0, "")
            self.SetFieldData("ChartIndexInBlock", "edate", 0, "")
            self.SetFieldData("ChartIndexInBlock", "Isamend", 0, "0")
            self.SetFieldData("ChartIndexInBlock", "Isgab", 0, "0")
            self.SetFieldData("ChartIndexInBlock", "IsReal", 0, "0")

            self.RequestService("ChartIndex", "")
            # time.sleep(2)
            QTest.qWait(2400)

    @classmethod
    def get_instance(cls):
        chartindex = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return chartindex



class Worker(QThread):

    def __init__(self):
        super().__init__()
        self.is_data_received = False
        self.sig_cl = Sig_cl()
        self.t0424 = t0424.get_instance()
        self.savedstockitem = Savedstockitem()
        self.chartindex = chartindex.get_instance()


    def run(self):

        while self.running:
        #while True:
            #now = datetime.datetime.now()

            rooppen_time = QTime(10, 10, 0)
            rclose_time = QTime(14, 30, 0)
            rcurrent_time = QTime.currentTime()

            if rooppen_time >= rcurrent_time:
                self.rtime = 120000
            elif rooppen_time < rcurrent_time:
                if rclose_time >= rcurrent_time:
                    self.rtime = 300000
                else:
                    self.rtime = 120000


            time = QTime.currentTime()
            print(time.toString())
            self.t0424.t0424_request()
            QTest.qWait(2000)
            print("akwsk")
            self.chartindex.chartindex_request_all()
            print("time is good")
            QTest.qWait(self.rtime) #1000 1초 60000 1분 300000 5분
            #self.sleep(12)
            self.savedstockitem.Save()
            print("hi" )

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()

        global search
        self.setupUi(self)  #qt디자이너에서 수정한 ui를 화면에 출력 가능하게해줌

        # self.kiwoom = Kiwoom() #키움 클래스 객체 생성
        self.xsession = XSession.get_instance() #로그인 인스턴스
        self.xsession.api_login() #로그인 함수호출

        self.xreal = XReal_S3__.get_instance() #S3 인스턴스
        self.xreal_K3 = XReal_K3__.get_instance() #K3 인스턴스
        self.t0424 = t0424.get_instance() #잔고 인스턴스
        self.t1102 = t1102.get_instance() #매수 종목 인스턴스

        self.chartindex = chartindex.get_instance() #차트인덱스 인스턴스
        self.order_stock = order_stock.get_instance()  # 주문 인스턴스

        self.savedstockitem = Savedstockitem() #데이터 저장된 클래스 객체 선언
        # self.save = Save_date()

        self.lineEdit.textChanged.connect(self.code_to_name) # 매수 코드 불러오기
        self.lineEdit_6.textChanged.connect(self.medo_to_name) #잔고 코드로 딕셔너리 불러오기
        self.pushButton_3.clicked.connect(self.medo_to_save) #딕서녀리에 익절,손절가 저장
        self.pushButton_4.clicked.connect(self.jipo_to_name) #딕셔너리에 차트인덱스 저장

        #self.pushButton_1.clicked.connect(self.real_time)
        self.pushButton_2.clicked.connect(self.jango_time) # 잔고 수신

        self.pushButton_5.clicked.connect(self.search_to_jango)  #매도 감시 버튼

        #self.stockgridview = stockgridview()

        self.xreal.sig_cl.sig_.connect(self.stockgridview) #메인창에 수신된 S3 실시간 데이터 출력
        self.xreal_K3.sig_cl.sig_.connect(self.stockgridview) #메인창에 수신된 K3 실시간 데이터 출력
        self.t0424.sig_cl.sig_.connect(self.stockgridview) #메인창에 수신된 잔고 데이터 출력
        self.t1102.sig_cl.sig_.connect(self.stockgridview)  # 메인창에 수신된 잔고 데이터 출력

        self.pushButton_1.clicked.connect(self.save_buy)  # 매수 딕셔너리 조회
        self.pushButton_6.clicked.connect(self.mesu_to_save)

        self.pushButton_7.clicked.connect(self.jipo_to_name_mesu)

        self.pushButton_8.clicked.connect(self.del_mesu)
        self.pushButton_16.clicked.connect(self.del_medo)

        self.pushButton_9.clicked.connect(self.update_grid)

        self.pushButton_10.clicked.connect(self.save_date)
        self.pushButton_11.clicked.connect(self.find_date)
        self.pushButton_12.clicked.connect(self.del_date)

        self.lineEdit_20.textChanged.connect(self.qunti_cal)
        self.lineEdit_21.textChanged.connect(self.rate_cal)

        self.pushButton_13.clicked.connect(self.start_chart)
        self.pushButton_14.clicked.connect(self.stop_chart)

        self.pushButton.clicked.connect(self.test)

        #self.pushButton_15.clicked.connect(self.ready_to_jango)


        self.worker = Worker()
        #self.worker.start()

        self.test()
        self.jango_time()

        QTest.qWait(2000)
        self.find_date()
        QTest.qWait(2000)
        self.update_grid()
        QTest.qWait(2000)
        self.search_to_jango()
        QTest.qWait(2000)
        self.start_chart()
        QTest.qWait(2000)
        self.search_to_jango()

        #print(cv2.__file__)


        """
        self.pushButton_1.clicked.connect(self.real_time)  #실시간 데이터 수신 버튼
        self.lineEdit.textChanged.connect(self.code_to_name) #종목코드 종목명으로 변경
        self.kiwoom.OnReceiveRealData.connect(self.kiwoom._receive_real_data) #실시간 수신된 데이터 수신 이벤트
        self.kiwoom.sig_cl.sig_.connect(self.stockgridview) #메인창에 수신된 실시간 데이터 출력
        """

        #self.scrnum = 5000 #화면 번호 초기값

    def test(self):

        print(self.savedstockitem.item_view)
        print(self.savedstockitem.item_jango)

    def code_to_name(self):
        stock_code = self.lineEdit.text()   # 입력한 글자 불러오는 메서드 text()

        self.xq_t1101 = XQuery_t1101.get_instance()
        stock_name = self.xq_t1101.request(stock_code)


        #stock_name = self.XQuery_t1101.request(stock_code) #종목코드로부터 종목명 출력하는 메서드

        self.lineEdit_2.setText(stock_name)   # 글자 표시하기 setText()

    def save_buy(self):
        #line 31
        stock_code = self.lineEdit.text()
        buy_value = self.lineEdit_2.text()
        bopenlowest_code = self.lineEdit_25.text()
        time_code = self.lineEdit_29.text()

        if (buy_value != ""):

            if stock_code not in self.savedstockitem.item_view.keys():
                self.savedstockitem.item_view[stock_code] = ['0종목코드', '1종목명', '2현재가', '3시가', '4고가', '5반등폭', '6신용여부', '7시가반영', '8거노고돌', '9거고돌', '10노고돌', '11수량', '12매수가', '13매수비율', '142', '15매수비율가','16고','17반등저점','18고돌거래량','19고돌','20매수비율가',bopenlowest_code, time_code, '23time', '24겝','25추매','26저','27손절금']
                #0.종목코드,,
                # 지표 1 - 저, 지표 2 - 고, 지표 3 - 반등저점, 지표 4 - 고돌거래량, 지표 5 - 고돌

                self.t1102.request(stock_code)

        else:

            self.error()
        self.stockgridview()

    def del_mesu(self):
        stock_code = self.lineEdit.text()

        if stock_code in self.savedstockitem.item_view.keys():
            del self.savedstockitem.item_view[stock_code]

            # 지표 1 - 저, 지표 2 - 고, 지표 3 - 반등저점, 지표 4 - 고돌거래량, 지표 5 - 고돌

        # if len(self.savedstockitem.item_view) != 0:
        #     print("view update")
        #
        #     item_cnt_v = len(self.savedstockitem.item_view)
        #
        #     print(self.savedstockitem.item_view)
        #
        #     scode_list_v = list(self.savedstockitem.item_view.keys())
        #
        #     self.tableWidget.setRowCount(item_cnt_v)
        #
        #
        #
        #     for i in range(item_cnt_v):
        #
        #         for j in range(15):
        #
        #             item = QTableWidgetItem(self.savedstockitem.item_view[scode_list_v[i]][j])
        #
        #             item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        #
        #             # 표 속성 가운데 정렬
        #             self.tableWidget.setItem(i, j, item)
        #             print("here2")
        self.stockgridview()

    def del_medo(self):
        stock_code = self.lineEdit_6.text()

        if stock_code in self.savedstockitem.item_jango.keys():
            del self.savedstockitem.item_jango[stock_code]

            # 지표 1 - 저, 지표 2 - 고, 지표 3 - 반등저점, 지표 4 - 고돌거래량, 지표 5 - 고돌

        # if len(self.savedstockitem.item_view) != 0:
        #     print("view update")
        #
        #     item_cnt_v = len(self.savedstockitem.item_view)
        #
        #     print(self.savedstockitem.item_view)
        #
        #     scode_list_v = list(self.savedstockitem.item_view.keys())
        #
        #     self.tableWidget.setRowCount(item_cnt_v)
        #
        #
        #
        #     for i in range(item_cnt_v):
        #
        #         for j in range(15):
        #
        #             item = QTableWidgetItem(self.savedstockitem.item_view[scode_list_v[i]][j])
        #
        #             item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        #
        #             # 표 속성 가운데 정렬
        #             self.tableWidget.setItem(i, j, item)
        #             print("here2")
        self.stockgridview()

    def jango_time(self):
        self.t0424.t0424_request()

        self.searchfirst = False
        self.savedstockitem.item_check["감시"] = 2
        """
        while self.xreal.count < 100:
            pythoncom.PumpWaitingMessages()
        """

    def jipo_to_name(self):

        self.chartindex.chartindex_request()

        #self.indexsearchfirst = False
        #self.savedstockitem.item_check["감시"] = 2

        #stock_name = self.XQuery_t1101.request(stock_code) #종목코드로부터 종목명 출력하는 메서드

        #self.lineEdit_2.setText(stock_name)

    def ready_to_jango(self):

        self.indexsearchfirst = False
        self.savedstockitem.item_check["감시"] = 2

        #stock_name = self.XQuery_t1101.request(stock_code) #종목코드로부터 종목명 출력하는 메서드

        #self.lineEdit_2.setText(stock_name)

    def jipo_to_name_mesu(self):

        m = self.lineEdit.text()
        self.chartindex.chartindex_request_mesu(m)

        #stock_name = self.XQuery_t1101.request(stock_code) #종목코드로부터 종목명 출력하는 메서드

        #self.lineEdit_2.setText(stock_name)

        # self.jipo_to_name_mesu

    def medo_to_name(self):
        medo_stock_code = self.lineEdit_6.text()   # 입력한 글자 불러오는 메서드 text()



        for i in self.savedstockitem.item_jango:
            a = str(i[1:])
            if medo_stock_code == i:
                self.lineEdit_7.setText(self.savedstockitem.item_jango[i][1])
                #print(self.savedstockitem.item_jango[i][0])


        #stock_name = self.XQuery_t1101.request(stock_code) #종목코드로부터 종목명 출력하는 메서드

        #self.lineEdit_2.setText(stock_name)

    def medo_to_save(self):
        medo_stock_code = self.lineEdit_6.text()  # 입력한 글자 불러오는 메서드 text()
        lose_stock_code = self.lineEdit_4.text()
        win_stock_code = self.lineEdit_5.text()
        pro_stock_code = self.lineEdit_17.text()  # 입력한 글자 불러오는 메서드 text()
        win_choice_code = self.lineEdit_18.text()
        lose_choice_code = self.lineEdit_19.text()
        medo_result_code = self.lineEdit_22.text()




        for i in self.savedstockitem.item_jango:
            a = str(i[1:])
            if medo_stock_code == i:
                self.savedstockitem.item_jango[i][9] = win_stock_code
                self.savedstockitem.item_jango[i][10] = lose_stock_code
                self.savedstockitem.item_jango[i][11] = pro_stock_code
                self.savedstockitem.item_jango[i][12] = win_choice_code
                self.savedstockitem.item_jango[i][13] = lose_choice_code
                self.savedstockitem.item_jango[i][14] = medo_result_code



                # print(self.savedstockitem.item_jango[i][0])

        # stock_name = self.XQuery_t1101.request(stock_code) #종목코드로부터 종목명 출력하는 메서드

        # self.lineEdit_2.setText(stock_name)
        self.stockgridview()

    def mesu_to_save(self):
        # line 31
        mesu_stock_code = self.lineEdit.text()  # 입력한 글자 불러오는 메서드 text()
        open_stock_code = self.lineEdit_9.text() #전일종가
        volume_stock_code = self.lineEdit_10.text()
        high_stock_code = self.lineEdit_11.text()
        mesuprice_stock_code = self.lineEdit_12.text()
        qunti_stock_code = self.lineEdit_13.text()
        mesurate_stock_code = self.lineEdit_14.text()
        sinyung_stock_code = self.lineEdit_15.text()
        high_choice_code = self.lineEdit_23.text()
        result_code = self.lineEdit_24.text()
        bopenlowest_code = self.lineEdit_25.text()
        time_code = self.lineEdit_29.text()
        gap_code = self.lineEdit_30.text()
        plus_buy_code = self.lineEdit_31.text()
        lose_money_code = self.lineEdit_20.text()


        for i in self.savedstockitem.item_view.keys():
            a = str(i[1:])
            if mesu_stock_code == i:

                self.savedstockitem.item_view[i][5] = high_choice_code
                self.savedstockitem.item_view[i][7] = open_stock_code
                self.savedstockitem.item_view[i][8] = volume_stock_code
                self.savedstockitem.item_view[i][9] = high_stock_code
                self.savedstockitem.item_view[i][10] = sinyung_stock_code
                self.savedstockitem.item_view[i][11] = qunti_stock_code
                self.savedstockitem.item_view[i][12] = mesuprice_stock_code
                self.savedstockitem.item_view[i][13] = mesurate_stock_code
                self.savedstockitem.item_view[i][14] = result_code
                self.savedstockitem.item_view[i][21] = bopenlowest_code
                self.savedstockitem.item_view[i][22] = time_code
                self.savedstockitem.item_view[i][23] = 0
                self.savedstockitem.item_view[i][24] = gap_code
                self.savedstockitem.item_view[i][25] = plus_buy_code
                self.savedstockitem.item_view[i][27] = lose_money_code

        self.savedstockitem.Save()
        self.stockgridview()

        # stock_name = self.XQuery_t1101.request(stock_code) #종목코드로부터 종목명 출력하는 메서드

        # self.lineEdit_2.setText(stock_name)

    def search_to_jango(self):

        try:
            if self.searchfirst == True:

                self.savedstockitem.item_check["감시"] = 1

                self.lineEdit_8.setText("감 시 중")
                self.searchfirst = False

                for i in self.savedstockitem.item_jango:

                    a = str(i[1:])

                    self.xreal.start(i) # 모의투자i
                    self.xreal_K3.start(i)

                for i in self.savedstockitem.item_view:

                    a = str(i[1:])

                    self.xreal.start(i)
                    self.xreal_K3.start(i)


            else:

                self.savedstockitem.item_check["감시"] = 2

                self.lineEdit_8.setText("중 지")
                self.searchfirst = True

                self.xreal.end()
                self.xreal_K3.end()
        except:
            print("오류")

    def update_grid(self):

        self.stockgridview()

    def save_date(self):
        self.savedstockitem.Save()

    def find_date(self):

        self.savedstockitem.Find()

    def del_date(self):
        self.savedstockitem.del_date()

    def error(self):
        QMessageBox.about(self, 'About Title', 'About Message')

    def qunti_cal(self):
        try:
            bill_input = self.lineEdit_20.text()   # 입력한 글자 불러오는 메서드 text()
            print(bill_input)
            self.scode = self.lineEdit.text()
            print(self.scode)
            mesu_input = self.lineEdit_21.text()
            print(mesu_input)
            #a = self.lineEdit.text()
            #print(self.savedstockitem.item_jango[self.scode][8])
            losep = (1-(float(mesu_input)-(float(self.savedstockitem.item_view[self.scode][20])*2.3))/float(mesu_input))*100
            print(losep)
            #now_num = self.savedstockitem.item_view[scode][2]

            #qunti = round(float(bill_input)/float(now_num))

            qunti = round(float(bill_input) / float(mesu_input) / ((float(losep) / 100)))

            self.lineEdit_13.setText(str(qunti))
        except:
            print("오류")

            #float(bill_input)/self.lineEdit_21.text()/(2*(losep/100))
            #float(bill_input) 손절금
            #self.lineEdit_21.text() 매수가
            # a = self.lineEdit.text() 코드
            #(self.lineEdit_21.text()-self.savedstockitem.item_jango[a][8])/self.lineEdit_21.text()*100  (매수가-손절가)/매수가*100  손절퍼센트


    def rate_cal(self):
        try:

            self.rate_input = self.lineEdit_21.text()   # 입력한 글자 불러오는 메서드 text()

            self.scode = self.lineEdit.text()


            저 = float(self.savedstockitem.item_view[self.scode][26])

            고 = float(self.savedstockitem.item_view[self.scode][16])


            매수비율 = round((1-((float(self.rate_input) - 저)/(고-저)))*1000)

            self.lineEdit_14.setText(str(매수비율))


        except:
            print("오류")

    def stop_chart(self):

        self.worker.pause()
        self.lineEdit_16.setText("INDEX 중 지")

    def start_chart(self):

        self.worker.resume()
        self.worker.start()
        self.lineEdit_16.setText("INDEX 감 시 중")



    """
    def real_time(self):
        for i in self.savedstockitem.item_jango:
            a = str(i[1:])
            self.xreal.start(a)
            while self.xreal.count < 100:
                pythoncom.PumpWaitingMessages()
    """
        #stock_code = self.lineEdit.text()  # 화면창에 입력된 종목코드



        # self.kiwoom.setrealreg(self.getnum(), stock_code, "9001;10", "0")  # 실시간 데이터를 달라고 하는 메서드

    """
    def real_time(self):
        stock_code = self.lineEdit.text()  # 화면창에 입력된 종목코드

        self.xreal.start(stock_code)
        while self.xreal.count < 100:
            pythoncom.PumpWaitingMessages()

        #self.kiwoom.setrealreg(self.getnum(), stock_code, "9001;10", "0")  # 실시간 데이터를 달라고 하는 메서드
    """

    def getnum(self):  #매번 화면 번호 바꿈으로서 오류 안나게함.
        if self.scrnum < 9999999999999999999999999999999999999999:
            self.scrnum += 1
        else:
            self.scrnum = 5000
        return int(self.scrnum)
    """
    def code_to_name(self):
        stock_code = self.lineEdit.text()   # 입력한 글자 불러오는 메서드 text()
        stock_name = self.kiwoom.get_master_code_name(stock_code) #종목코드로부터 종목명 출력하는 메서드
        self.lineEdit_2.setText(stock_name)   # 글자 표시하기 setText()

    def real_time(self):
        stock_code = self.lineEdit.text() #화면창에 입력된 종목코드
        self.kiwoom.setrealreg(self.getnum(), stock_code, "9001;10", "0")  #실시간 데이터를 달라고 하는 메서드

    """

    def stockgridview(self):

        self.tableWidget.setRowCount(0)

        if len(self.savedstockitem.item_jango) != 0:
            self.tableWidget_2.setRowCount(0)

            item_cnt = len(self.savedstockitem.item_jango)

            scode_list = list(self.savedstockitem.item_jango.keys())

            self.tableWidget_2.setRowCount(item_cnt)


            for i in range(item_cnt):

                for j in range(15):

                    item = QTableWidgetItem(str(self.savedstockitem.item_jango[scode_list[i]][j]))

                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)

                    # 표 속성 가운데 정렬
                    self.tableWidget_2.setItem(i, j, item)



        if len(self.savedstockitem.item_view) != 0:
            # line 31
            self.tableWidget.setRowCount(0)



            item_cnt_v = len(self.savedstockitem.item_view)



            scode_list_v = list(self.savedstockitem.item_view.keys())



            self.tableWidget.setRowCount(item_cnt_v)



            for i in range(item_cnt_v):


                for j in range(16):



                    item = QTableWidgetItem(str(self.savedstockitem.item_view[scode_list_v[i]][j]))


                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)

                    # 표 속성 가운데 정렬
                    self.tableWidget.setItem(i, j, item)



                # 표 속성 가운데 정렬





    """
    def stockgridview(self):
        item_cnt = len(self.savedstockitem.item_view)
        scode_list = list(self.savedstockitem.item_view.keys())
        self.tableWidget.setRowCount(item_cnt)
        for i in range(item_cnt):
            for j in range(4):
                item = QTableWidgetItem(self.savedstockitem.item_view[scode_list[i]][j])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter) #표 속성 가운데 정렬
                self.tableWidget.setItem(i, j, item)
                
    """



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    #os.execl(sys.executable, sys.executable, *sys.argv)


