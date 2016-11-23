import configparser as ConfigParser


class ContextConfigReader(object):

    def __init__(self):
        pass

    @staticmethod
    def context_config_reader(option):
        config = ConfigParser.ConfigParser()
        config.read("/home/fahim/Desktop/test_1/temp/contextConfigFile")
        return config.get('context', option)

