# -*- coding:utf-8 -*-
# need install sendmail
import smtplib as SMTP
from email.mime.text import MIMEText
from email.header import Header
from code.app.post.conf.config_loader import CONF

import code.app.post.app_project as app_post
global v2log

def send_email_info(data, title="新的消息"):
    receivers = []
    v2log = app_post.get_logger()
    conf = CONF.load_post_cfg(app_post.get_app_config_path()+"/post.json")
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
        v2log.error("[email]conf don't exist, can't send: \n"+data)
        return False

    # exception para adjust
    if len(email_conf["sender"]) <= 0:
        v2log.warn("no email box to send.")
        return False
    for _recv in email_conf["receiver"]:
        if _recv["email"] != None:
            receivers.append(_recv["email"])
    if len(receivers) <= 0:
        v2log.warn("no receivers to accept.")
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
            v2log.info("【成功】邮件发送成功, [%s] to %s" % (e['email'], receivers))
            return True
        except SMTP.SMTPException as ex:
            v2log.error("【错误】无法发送邮件 [%s] to %s, Error: %s" % (e['email'], receivers, ex))
    return False


# for debug
if __name__ == '__main__':
    send_email_info("123")
