from code.post.self_email import send_email_info
from code.post.server_channel import send_server_channel


def send_email(content, title):
    return send_email_info(content, title)


def send_svchannel(content, title):
    return send_server_channel(title, content)