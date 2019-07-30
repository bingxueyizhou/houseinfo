import json
import os
import shutil
import codecs


class CONF(object):
    PATH_DIR_CONFIG_POST = '/post'
    PATH_FILE_CONFIG_POST = PATH_DIR_CONFIG_POST+'/post.json'
    PATH_FILE_CONFIG_POST_ORI = PATH_DIR_CONFIG_POST+'/ori.post.json'

    @staticmethod
    def __load_file_cfg(ori, cfg):
        # transfer path
        class_dir = os.path.dirname(__file__)
        ori = class_dir + ori
        cfg = class_dir + cfg

        if os.path.isfile(cfg) is False:
            shutil.copyfile(ori, cfg)

        try:
            with codecs.open(cfg, 'r', encoding='utf-8') as json_f:
                return json.loads(json_f.read())
        except Exception as e:
            print(e)

        return None

    '''
    {
        "debug":1,
        "protocol":[
            {
                "name": "svchannel",
                "keys": ["__modify__"]
            },
            {
                "name": "email",
                "sender":[
                    {"email":"__modify__", "pwd":"__modify__", "smtp":"__modify__"}
                  ],
                  "receiver":[
                    {"name":"__modify__", "email":"__modify__"}
                  ]
            }
        ]
    }
    '''
    @staticmethod
    def load_post_cfg():
        # default value
        config = dict()
        config['debug'] = True
        config['protocol'] = []

        ret = CONF.__load_file_cfg(CONF.PATH_FILE_CONFIG_POST_ORI, CONF.PATH_FILE_CONFIG_POST)
        if ret is not None:
            return ret
        return config


# for debug
if __name__ == '__main__':
    cfg = CONF()
    print(CONF.load_post_cfg())
