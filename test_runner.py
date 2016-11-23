from config_reader import ConfigReader as config
import subprocess
import sys
import os
import shutil
import zipfile


def run_test(instances):


    """
    adb
     -s
     192.168.56.101:5555
     shell
     am
     instrument
     -w
     -e
     class
     com.example.android.notepad.NotePadTest com.example.android.notepad.test/android.test.InstrumentationTestRunner
    :return:
    """

    for instance in instances:
        adb = config.config_file_reader('adb')
        directory = config.config_file_reader('directory')
        #print(adb)
        apk = config.config_file_reader('apk')
        #print(directory + apk)
        test_class = config.config_file_reader('test_class')
        test_method = config.config_file_reader('test_method')
        #print(test_method)
        print(subprocess.check_output([adb, '-s', 'emulator-'+instance.port, 'shell', 'am','instrument', '-w', '-r', '-e', 'debug', 'false','-e','class', test_class, test_method]))


def test(uid, project_name):
    gradle_path = os.getcwd() + '/' + project_name
    os.chdir(gradle_path)
    os.system('chmod +777 ' + gradle_path + '/gradlew')
    # print(str(subprocess.check_output([gradle_path, 'tasks', 'connectedAndroidTest'])))
    command = './gradlew tasks connectedAndroidTest'
    os.system(command)
    process_result(uid, project_name)
    uid_zip = uid + '.zip'
    subprocess.check_output(['zerorpc', "tcp://10.100.106.120:4244", 'fetch', uid_zip])


def process_result(uid, project_name):
    os.chdir('..')
    base_dir = os.getcwd()
    folder_path = os.getcwd() + '/' + project_name + '/app/build/reports/androidTests/connected/'
    zipfile_name = 'result.zip'
    os.chdir(folder_path)
    path1 = os.getcwd()
    os.chdir(base_dir)
    subprocess.check_output(['python', '-m', 'zipfile', '-c', zipfile_name, path1])
    zip_ref = zipfile.ZipFile(os.getcwd() + '/' + zipfile_name, 'r')
    zip_ref.extractall(os.getcwd())
    zip_ref.close()
    os.unlink(zipfile_name)
    os.rename(os.getcwd()+'/connected', os.getcwd()+'/result')
    zip_dir = os.getcwd()
    os.chdir('..')
    subprocess.check_output(['python', '-m', 'zipfile', '-c', uid + '.zip', zip_dir])
    # shutil.rmtree(os.getcwd() + '/temp')
    # os.makedirs(os.getcwd() + '/temp')


if __name__ == '__main__':
    test()
