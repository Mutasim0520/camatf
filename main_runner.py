from config_reader import ConfigReader as config

import emulator_manager as emulator
import app_manager
import test_runner
import os
import shutil


def main1(uid):
    #print(config.config_file_reader('emulator'))
    uid = "mostaque#1479870945"
    process_file(uid)
    emulator.get_context()
    # emulator.create_emulator()

    # if flag:
    #     flag =
    flag = emulator.emulator_runner()
    # else:
    #     print("Emulator could not be created")
    # instances = emulator.instances_manager()
    # for instance in instances:
    #     print(instance)
    # app_manager.app_installer(instances)
    if flag:
        test_runner.test(uid, project_name='testProject')
    # emulator.kill_emulator()


def process_file(uid):
    source = os.getcwd() + '/' + uid + '.zip';
    destination = os.getcwd() + '/temp/' +uid + '.zip';
    shutil.move(source, destination)
    temp_path = os.getcwd() + '/temp'
    os.chdir(temp_path)
    source = uid + '.zip'
    print(temp_path)
    shutil.unpack_archive(source)
    os.unlink(os.getcwd() + '/' + uid + '.zip')
    path = os.getcwd() + '/' + uid + '/' + uid
    destination1 = os.getcwd() + '/'
    files = os.listdir(path)
    for f in files:
        shutil.move(path + '/' +f, destination1)
    shutil.rmtree(os.getcwd() + '/' + uid)


if __name__ == '__main__':
    uid = "mostaque#1479702495"
    main1(uid)
