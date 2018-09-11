# -*- coding:utf-8 -*-
# need install sendmail
import smtplib as SMTP
from email.mime.text import MIMEText
from email.header import Header
from config import CONF


def send_house_info(data):
    receivers = []
    conf = CONF.load_email_cfg()
    if conf["debug"]:
        print("debug email: \n"+data)
        return True

    # exception para adjust
    if len(conf["sender"]) <= 0:
        print("no email box to send.")
        return False
    for _recv in conf["receiver"]:
        if _recv["email"] != None:
            receivers.append(_recv["email"])
    if len(receivers) <= 0:
        print("no receivers to accept.")
        return False

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText("为你推送更新的【成都】新盘信息：\n"+
                        data, 'plain', 'utf-8')
    for e in conf["sender"]:
        message['From'] =  e['email']
        message['To']   =  ','.join(receivers)
        message['cc']   =  ','.join(receivers)

        message['Subject'] = Header('【成都】新盘信息', 'utf-8')
        try:
            server = SMTP.SMTP_SSL(e['smtp'], 465)
            server.login(e['email'], e['pwd'])
            # print message.as_string()
            # return
            server.sendmail(e['email'], receivers, message.as_string())
            print("【成功】邮件发送成功, [%s] to %s" % (e['email'], receivers))
            return True
        except SMTP.SMTPException as ex:
            print("【错误】无法发送邮件 [%s] to %s, Error: %s" % (e['email'], receivers, ex))
    return False


if __name__ == '__main__':
    send_house_info("123")
