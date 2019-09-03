import code.app.post.app_project as app_post
from code.app.post.server_channel import send_server_channel as send_svchannel

if __name__ == '__main__' :
    app_post.app_init()
    send_svchannel("hello")