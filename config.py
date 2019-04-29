import json
import os
import shutil
import codecs


class CONF(object):
    EMAIL_CONFIG_PATH='./config/email.json'
    EMAIL_ORI_CONFIG_PATH='./config/email.ori.json'
    SERVER_CHANNEL_CONFIG_PATH='../config/server_channel.json'
    SERVER_CHANNEL_ORI_CONFIG_PATH='config/server_channel.ori.json'

    """
        return:
          "debug":1,  just print not send
          "sender":[
            {"email":"", "pwd":"", "smtp":""}
          ],
          "receiver":[
            {"name":"", "email":"" }
          ]
          "server_channel":[
            {"key":""}
          ]
    """
    @staticmethod
    def load_email_cfg():
        config = dict()
        config['sender'] = []
        config['debug'] = True
        config['receiver'] = []
        if os.path.isfile(CONF.EMAIL_CONFIG_PATH):
            try:
                with codecs.open(CONF.EMAIL_CONFIG_PATH, 'r', encoding='utf-8') as json_f:
                    return json.loads(json_f.read())
            except Exception as e:
                print(e)
                return config
        else:
            shutil.copyfile(CONF.EMAIL_ORI_CONFIG_PATH, CONF.EMAIL_ORI_CONFIG_PATH)
        return config

    """
        return:
          "debug":1,  just print not send
          "keys":[
            "",
          ]
    """
    @staticmethod
    def load_server_channel_cfg():
        config = dict()
        config['debug'] = True
        config['keys'] = []
        if os.path.isfile(CONF.SERVER_CHANNEL_CONFIG_PATH):
            try:
                with codecs.open(CONF.SERVER_CHANNEL_CONFIG_PATH, 'r', encoding='utf-8') as json_f:
                    return json.loads(json_f.read())
            except Exception as e:
                print(e)
                return config
        else:
            shutil.copyfile(CONF.SERVER_CHANNEL_CONFIG_PATH, CONF.SERVER_CHANNEL_ORI_CONFIG_PATH)
        return config