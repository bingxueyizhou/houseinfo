import json
import os
import shutil
import codecs


class CONF(object):
    EMAIL_CONFIG_PATH='./config/email.json'
    EMAIL_ORI_CONFIG_PATH='./config/email.ori.json'

    """
        return:
          "debug":1,  just print not send
          "sender":[
            {"email":"", "pwd":"", "smtp":""}
          ],
          "receiver":[
            {"name":"", "email":"" }
          ]
    """
    @staticmethod
    def load_email_cfg():
        config = dict()
        config['sender'] = []
        config['is_debug'] = True
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