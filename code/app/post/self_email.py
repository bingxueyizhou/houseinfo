# -*- coding:utf-8 -*-
# need install sendmail
import smtplib as SMTP
from email.mime.text import MIMEText
from email.header import Header
from conf.config_loader import CONF


def send_email_info(data, title="新的消息"):
    receivers = []
    conf = CONF.load_post_cfg()
    if conf["debug"]:
        print("[email] debug print: \n"+data)
        return True

    # confirm email protocol.
    email_conf = None
    for p in conf["protocol"]:
        if p["name"] == "email":
            email_conf = p
            break
    if email_conf is None:
        print("[email]conf don't exist, can't send: \n"+data)
        return False

    # exception para adjust
    if len(email_conf["sender"]) <= 0:
        print("no email box to send.")
        return False
    for _recv in email_conf["receiver"]:
        if _recv["email"] != None:
            receivers.append(_recv["email"])
    if len(receivers) <= 0:
        print("no receivers to accept.")
        return False

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(data, 'plain', 'utf-8')
    for e in email_conf["sender"]:
        message['From'] =  e['email']
        message['To']   =  ','.join(receivers)
        message['cc']   =  ','.join(receivers)

        message['Subject'] = Header(title, 'utf-8')
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


# for debug
if __name__ == '__main__':
    send_email_info("123")
