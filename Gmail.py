import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(mail: str) -> None:

    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    # gmail pw 가져오기
    with open('./Email/App.txt','r') as f:
        my_pw = f.readline()

    # log in
    my_id = 'woohyeop0998@gmail.com'
    smtp.login(my_id, my_pw)

    # 메일 기본 정보 설정
    msg = MIMEMultipart()
    msg['Subject'] = f'학부연구생 총 데이터'
    msg['From'] = 'woohyeop0998@gmail.com'
    msg['To'] = mail

    file_list = os.listdir('./undergraduate research student/')

    for i in file_list:
        with open(f'./undergraduate research student/{i}', 'rb') as csv_file:
            attachment = MIMEApplication(csv_file.read())
            attachment.add_header('Content-Disposition','attachment',filename=i)
            msg.attach(attachment)

    smtp.sendmail(my_id,mail,msg.as_string())
    smtp.quit()

    # 뭔가 수정했어요