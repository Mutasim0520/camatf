import subprocess
from emulator import Emulator
from config_reader import ConfigReader as config
import emulator_manager as emulator

"""
/home/amit/Android/Sdk/platform-tools/adb
-s
5554:nexus_4
install
/home/amit/git/context_based_mobile_app_testing/ExampleTestProject_AndroidStudio_v5.3/app/build/outputs/apk/app-debug.apk
"""

# def get_installde_app_port(emulator_inctances):

def app_installer(emulator_instances):
    # print emulator_instances
    adb = config.config_file_reader('adb')
    directory = config.config_file_reader('directory')
    #print(adb)
    apk = config.config_file_reader('apk')
    #print(directory + apk)
    installed_app_port = {}
    for instance in emulator_instances:
        #print instance
        emulator_port =  instance.port
        if (emulator_port not in installed_app_port):
            # string = "app is not there"
            string = subprocess.check_output([adb, '-s', 'emulator-' + emulator_port, 'install', directory + apk])
            installed_app_port.update({emulator_port : apk})
            print (string)

        else:
            print ("app is there")
    # return installed_app_port
