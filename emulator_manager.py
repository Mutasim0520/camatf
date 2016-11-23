from config_reader import ConfigReader as config
from contextConfig_reader import ContextConfigReader as c_config
import subprocess
from emulator import Emulator
from subprocess import Popen, PIPE
import syslog
import time

emulator_processes = []


emulator_processes = []
context_list = {}

def get_context():
    list1 = ['emulator_name','abi','android_version','net_speed','net_delay','cpu_delay','Screen_orientation']
    i = 0
    for items in list1:
        command = c_config.context_config_reader(str(list1[i]))
        context_list.update({list1[i]: command})
        i += 1
    print(context_list)

def create_emulator():
    android = config.config_file_reader('android')
    target_id = 5
    emulator_create = subprocess.Popen([android,'create', 'avd', '-n', context_list['emulator_name'], '-t', str(target_id), '-b', context_list['abi']],stdin=subprocess.PIPE)
    stri = str('n').encode('utf-8')
    emulator_create.stdin.write(stri)
    return emulator_create

def get_avd_list():
    command = config.config_file_reader('emulator')
    avd = str(subprocess.check_output([command, 'emulator', '-list-avds']))
    avd = avd.split('\n')
    avd.pop(-1)
    return avd


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
	# //emulator port empty hole emulator chole na
    return emulator_ports

def kill_emulator():
    android = config.config_file_reader('android')
    process =subprocess.Popen([android,'delete','avd','-n',context_list['emulator_name']])

def check_avd_botted_completely(emulator_port):
    port = "emulator-"
    port = port + str(emulator_port)

    adb = config.config_file_reader('adb')
    print(port)
    print ("going to sleep")
    time.sleep(20)
    i=0
    while (True):
        check = str(subprocess.check_output([adb, '-s', port, 'shell', 'getprop', 'sys.boot_completed']))
        check = check.strip('b\'')
        check = check.strip('\\r')
        check = check.strip('\\n')
        check = check.strip()
        print(check)
        if check == "1":
            print ("completed")
            return 1
        time.sleep(2)
        i=i+1
        print("wait"+str(i))
    # check = int(check)
    # return check


def check_running_avd():
    avds = config.avd_file_reader()
    avds.pop(-1)
    instances = instances_manager()
    runnig_emulator_model = []
    valid_model = []
    for instance in instances:
        runnig_emulator_model.append(instance.model)
    for item in avds:
        if item in runnig_emulator_model:
            pass
        else:
            valid_model.append(item)
    return valid_model


def emulator_runner():
    print (context_list['emulator_name'])

    # adb = config.config_file_reader('adb')
    # p = subprocess.Popen([adb,'start-server'])

    # avds = check_running_avd()
    # if avds:
    #     emulator_port = get_running_avd_port()
    #     if emulator_port:
    #         emulator_port = int(emulator_port[-1]) + 2
    #     else:
    emulator_port = 5555
        # print(emulator_port)
        #
        # The console port number must be an even integer between 5554 and 5584,
        # inclusive. <port>+1 must also be free and will be reserved for ADB.

        #########################################################
        # for name in avds:
        #     print(name)
    command = config.config_file_reader("emulator")
        # command_argument = " -avd " + name
        #     print(command_argument)
        #     print(command + command_argument)
    current_process = subprocess.Popen([command,'-port', str(emulator_port),'-avd',context_list['emulator_name']], stdout=subprocess.PIPE)
            # print(current_process.pid, emulator_port)
    check = check_avd_botted_completely(emulator_port)
    if check == 1:
        print ( context_list['emulator_name']+ " has booted cpmpletely")
        flag = True
        return flag
    else:
        print (context_list['emulator_name'] + " has not booted cpmpletely")
        flag = False
        return flag
    #         emulator_port += 2
    #         emulator_processes.append(current_process)
    # else:
    #     print ("all AVD is allready running")




def get_name(uid):
    path = os.getcwd() + '/temp/' + uid + '/' + uid + '/context'
    with open(path, 'r') as f:
        first_line = f.readline()
    return first_line


def instances_manager():
    adb = config.config_file_reader('adb')
    adb_devices = str(subprocess.check_output([adb, 'devices']))
    # print(adb_devices)
    adb_devices = adb_devices.split('\n')
    # print(adb_devices)
    adb_devices = adb_devices[1:]
    # print(adb_devices)
    emulator_ports = []
    emulators = []
    for adb_device in adb_devices:
        emulator_port = adb_device.split('\t')[:1][0][9:]
        # print ("hello")
        # print adb_device.split('\t')[:1][0][9:]
        if (len(emulator_port) > 3):
            emulator_ports.append(emulator_port)
            # pid = str(subprocess.check_output(['netstat', '-tulpn' ,'|', 'grep', emulator_port]))[9:]
            # print(emulator_port, len(emulator_port), pid)
            # print(emulator_port)
            pid = str(subprocess.check_output(['lsof', '-i', 'tcp:' + emulator_port])).split('\n')[1:][0].split(' ')[1]
            # print(pid)
            device_details_in_ps = str(subprocess.check_output(['ps', pid]))
            # print (device_details_in_ps)
            model = get_device_emulator_model(device_details_in_ps)
            # print(model)

            current_emulator = Emulator(emulator_port, pid, model)
            emulators.append(current_emulator)
            # print(current_emulator)
    return emulators


def get_device_emulator_model(output_raw):
    # print(output_raw)
    """
    PID TTY      STAT   TIME COMMAND
    15522 tty2     Rl+  128:13 /home/amit/Android/Sdk/tools/emulator64-x86 -port 5557 -avd nexus_s
    """
    current_string = output_raw.split('\n')[1:][:1][0]

    """
    15521 tty2     Rl+  134:48 /home/amit/Android/Sdk/tools/emulator64-x86 -port 5555 -avd nexus_4
    """
    index_of_avd = current_string.index('-avd')
    """
    nexus_s
    """
    return current_string[index_of_avd + 5:]
