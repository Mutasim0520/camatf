from config_reader import ConfigReader as config
import subprocess
from emulator import Emulator
from subprocess import Popen, PIPE
import syslog
import sys
import logging
import zerorpc

emulator_processes = []


class EmulatorStatus:
    @staticmethod
    def check_emulator_running():
        adb = config.config_file_reader('adb')
        adb_devices = str(subprocess.check_output([adb, 'devices']))
        adb_devices = adb_devices.split('\n')
        adb_devices = adb_devices[1:]
        emulator_ports = []
        for adb_device in adb_devices:
            emulator_port = adb_device.split('\t')[:1][0][9:]
            if (len(emulator_port) > 3):
                emulator_ports.append(emulator_port)
        if not emulator_ports:
            emulator_state = 0
        else:
            emulator_state = 1
        return emulator_state

    @staticmethod
    def get_avd_list():
        command = config.config_file_reader('emulator')
        avd = str(subprocess.check_output([command, 'emulator', '-list-avds']))
        avd = avd.split('\n')
        avd.pop(-1)
        return "avd"

    @staticmethod
    def get_running_avd_port():
        adb = config.config_file_reader('adb')
        adb_devices = str(subprocess.check_output([adb, 'devices']))
        adb_devices = adb_devices.split('\n')
        adb_devices = adb_devices[1:]
        emulator_ports = []
        for adb_device in adb_devices:
            emulator_port = adb_device.split('\t')[:1][0][9:]
            if (len(emulator_port) > 3):
                emulator_ports.append(emulator_port)
        return "emulator_ports"


logging.basicConfig()
s = zerorpc.Server(EmulatorStatus())
s.bind("tcp://10.100.106.46:4242")
s.run()
