import smtplib
from email.mime.multipart import MIMEMultipart # 메일의 Data 영역의 메시지를 만드는 모듈
from email.mime.text import MIMEText # 메일의 본문 내용을 만드는 모듈
from email.mime.application import MIMEApplication # 메일의 첨부 파일을 base64 형식으로 변환
from email.mime.image import MIMEImage # 메일의 이미지 파일을 base64 형식으로 변환
import smtplib
from email.mime.text import MIMEText
def sendmail():


    # 587포트 및 465포트 존재
    smtp = smtplib.SMTP('smtp.gmail.com', 587)

    smtp.ehlo()

    smtp.starttls()

    # 로그인을 통해 지메일 접속
    smtp.login('vcxz1245@gmail.com', 'kquu jwfy abeh kzpt')

    # 내용을 입력하는 MIMEText => 다른 라이브러리 사용 가능
    msg = MIMEText('내용 : 본문 내용')
    msg['Subject'] = '제목: 파이썬으로 gmail 보내기'

    # 이메일을 보내기 위한 설정(Cc도 가능)
    smtp.sendmail('vcxz1245@gmail.com', 'strademart@naver.com', msg.as_string())

    # 객체 닫기
    smtp.quit()


sendmail()

#kquu jwfy abeh kzpt