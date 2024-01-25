from Controller import *
import pickle
from PyQt5.QAxContainer import *
import os

class Savedstockitem(QAxWidget):
    item_view = {}
    item_jango = {}
    item_check = {}
    item_index = {}


    def Save(self):
        with open('view.pkl','wb') as f:
            print(self.item_view)
            pickle.dump(self.item_view, f)
        # with open('jango.pkl', 'wb') as f:
        #     pickle.dump(self.savedstockitem.item_jango, f)

        with open('jango.pkl','wb') as f:
            print(self.item_jango)
            pickle.dump(self.item_jango, f)
        # with open('jango.pkl', 'wb') as f:
        #     pickle.dump(self.savedstockitem.item_jango, f)

    def Find(self):

        try:
            with open('view.pkl', 'rb') as f:

                print("1")
                self.item_view1 = pickle.load(f)
                print("1")
                print(self.item_view1.keys())

                for key in self.item_view1.keys():


                    self.item_view[key] = ['0종목코드','1종목명','2현재가','3시가','4고가','5반등폭','6신용여부','7시가반영','8거노고돌','9거고돌','10노고돌','11수량','12매수가','13매수비율','14결과','@매수비율가','@고','@고돌저점','@고돌거래량','@고돌','@반등폭','@장전최저','22시간','23time','24갭','25추매','26저','27손절금']
                    print(str(self.item_view1[key][19]))
                    self.item_view[key][0] = str(self.item_view1[key][0])
                    self.item_view[key][1] = str(self.item_view1[key][1])
                    self.item_view[key][2] = str(self.item_view1[key][2])
                    self.item_view[key][3] = str(self.item_view1[key][3])
                    self.item_view[key][4] = str(self.item_view1[key][4])
                    self.item_view[key][5] = str(self.item_view1[key][5])
                    self.item_view[key][6] = str(self.item_view1[key][6])
                    self.item_view[key][7] = str(self.item_view1[key][7])
                    self.item_view[key][8] = str(self.item_view1[key][8])
                    self.item_view[key][9] = str(self.item_view1[key][9])
                    self.item_view[key][10] = str(self.item_view1[key][10])
                    self.item_view[key][11] = str(self.item_view1[key][11])
                    self.item_view[key][12] = str(self.item_view1[key][12])
                    self.item_view[key][13] = str(self.item_view1[key][13])
                    self.item_view[key][14] = str(self.item_view1[key][14])
                    self.item_view[key][15] = str(self.item_view1[key][15])
                    self.item_view[key][16] = str(self.item_view1[key][16])
                    self.item_view[key][17] = str(self.item_view1[key][17])
                    self.item_view[key][18] = str(self.item_view1[key][18])
                    self.item_view[key][19] = str(self.item_view1[key][19])
                    self.item_view[key][20] = str(self.item_view1[key][20])
                    self.item_view[key][21] = str(self.item_view1[key][21])
                    self.item_view[key][22] = str(self.item_view1[key][22])
                    self.item_view[key][23] = str(self.item_view1[key][23])
                    self.item_view[key][24] = str(self.item_view1[key][24])
                    self.item_view[key][25] = str(self.item_view1[key][25])
                    self.item_view[key][26] = str(self.item_view1[key][26])
                    self.item_view[key][27] = str(self.item_view1[key][27])


                    print(self.item_view)

            with open('jango.pkl', 'rb') as f:

                print("2")
                self.item_jango1 = pickle.load(f)
                print("2")
                print(self.item_jango1.keys())

                for key in self.item_jango1.keys():
                    print("2")
                    # del self.item_jango[key]
                    print("2")
                    self.item_jango[key] = ['0종목코드','1종목명','2현재가','3매수가','4수량','5신용','6대출일','7자동익절가','8자동손절가','9수동익절가','10수동손절가','11프로익절가','12익절선택','13손절선택','14결과','@최저점','@당시가']
                    print(str(self.item_jango1[key][15]))
                    self.item_jango[key][0] = str(self.item_jango1[key][0])
                    self.item_jango[key][1] = str(self.item_jango1[key][1])
                    self.item_jango[key][2] = str(self.item_jango1[key][2])
                    self.item_jango[key][3] = str(self.item_jango1[key][3])
                    self.item_jango[key][4] = str(self.item_jango1[key][4])
                    self.item_jango[key][5] = str(self.item_jango1[key][5])
                    self.item_jango[key][6] = str(self.item_jango1[key][6])
                    self.item_jango[key][7] = str(self.item_jango1[key][7])
                    self.item_jango[key][8] = str(self.item_jango1[key][8])
                    self.item_jango[key][9] = str(self.item_jango1[key][9])
                    self.item_jango[key][10] = str(self.item_jango1[key][10])
                    self.item_jango[key][11] = str(self.item_jango1[key][11])
                    self.item_jango[key][12] = str(self.item_jango1[key][12])
                    self.item_jango[key][13] = str(self.item_jango1[key][13])
                    self.item_jango[key][14] = str(self.item_jango1[key][14])
                    self.item_jango[key][15] = str(self.item_jango1[key][15])
                    self.item_jango[key][16] = str(self.item_jango1[key][16])



                    print(self.item_jango)
        except:
            print("없다")

    def del_date(self):
        print("된다")
        file = './view.pkl'
        file1 = './jango.pkl'
        print("된다")
        if (os.path.isfile(file)) or (os.path.isfile(file1)):
            try:
                os.remove('./view.pkl')
                os.remove('./jango.pkl')

            except:
                print("없네")
#
# class Save_date(QAxWidget):
#     def __init__(self):
#         super().__init__()
#         self.savedstockitem = Savedstockitem()
#
#
#     def Save(self):
#         with open('view.pkl','wb') as f:
#             print(self.savedstockitem.item_view)
#             pickle.dump(self.savedstockitem.item_view, f)
#         # with open('jango.pkl', 'wb') as f:
#         #     pickle.dump(self.savedstockitem.item_jango, f)
#
#     def Find(self):
#         with open('view.pkl', 'rb') as f:
#             # print(pickle.load(f))
#             self.savedstockitem.item_view = pickle.load(f)
#             print(self.savedstockitem.item_view)
#
#     def del_date(self):
#         print("삭제")

#


