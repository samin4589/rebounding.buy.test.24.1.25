import win32com.client
import pythoncom
import time

import xing_login


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

        if err_code < 0:
            print("error... {0}".format(err_code)) # data 요청하기 --  연속조회인경우만 True

    @classmethod
    def get_instance(cls):
        xq_t1101 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return xq_t1101


class XReal_S3_:
    def __init__(self):
        super().__init__()
        self.count = 0

    def OnReceiveRealData(self, tr_code):  # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count = 1
        stockcode = self.GetFieldData("OutBlock", "shcode")
        price = self.GetFieldData("OutBlock", "price")
        chetime = self.GetFieldData("OutBlock", "chetime")
        print(self.count, stockcode, price, chetime)
        print(".... 실시간 TR code => {0}".format(tr_code))

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
            """
            if xreal.count == 5:
                xreal.add_item("003490")  # 대한항공 실시간 조회 추가

            if xreal.count == 20:
                xreal.remove_item("005930")  # 삼성전자 실시간 조회 제거

            if xreal.count == 30:
                xreal.end()  # 실시간 조회 중단.
                time.sleep(10)
                print("---- end -----")
                break
            """

    xsession = xing_login.XSession.get_instance()
    xsession.api_login()

    get_single_data("105840")
    get_real_data("105840")
