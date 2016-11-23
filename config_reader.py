import configparser as ConfigParser


class ConfigReader(object):

    def __init__(self):
        pass

    @staticmethod
    def config_file_reader(option):
        config = ConfigParser.ConfigParser()
        config.read("/home/fahim/Desktop/test_1/configFile")
        print (config.get('emulator', option))
        return config.get('emulator', option)

    @staticmethod
    def avd_file_reader():
        avd_path = ConfigReader.config_file_reader('avds')
        txt = open(avd_path)
        avds = txt.read().split('\n')
        return avds
