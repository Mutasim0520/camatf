import socket
import zerorpc
import main_runner


class FileFetch:

    @staticmethod
    def fetch(filename):
        host = '10.100.106.120'
        port = 5000
        filename = str(filename, 'utf-8')
        s = socket.socket()
        s.connect((host, port))
        print(filename)

        if filename != 'q':
            s.send(filename.encode('utf-8'))
            data = s.recv(1024).decode('utf-8')
            if data[:6] == 'EXISTS':
                filesize = int(data[6:])
                message = "Y"
                if message == 'Y':
                    s.send(("OK").encode('utf-8'))
                    new_filename = filename.rsplit('/', 1)
                    f = open(new_filename[1], 'wb')
                    data = s.recv(1024)
                    totalRecv = len(data)
                    f.write(data)
                    while totalRecv < filesize:
                        data = s.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                        print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done")
                    print("Download Complete!")
                    f.close()
            else:
                print("File Does Not Exist!")

        s.close()

        new_filename = filename.rsplit('/', 1)
        uid = str(new_filename[1])[:-4]
        main_runner.main1(uid)


# if __name__ == '__main__':
#     FileFetch.fetch(filename)

s = zerorpc.Server(FileFetch())
s.bind("tcp://10.100.106.46:4243")
s.run()
