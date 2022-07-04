import time
import threading
import paramiko


class TestThread(threading.Thread):
    def __init__(self, ip, port='22', username='root', password='root'):
        super(TestThread, self).__init__()
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

        try:
            self.transport = paramiko.Transport((self.ip, 22))
            self.transport.connect(username='root', password='root')
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except BaseException as e:
            print(e)
            raise Exception('连接失败')

    def file_download(self, remotepath='/home/dell/2019-05-28-15-36-07.dat', localpath='1.txt'):
        print('Download file: {} --> {}'.format(remotepath, localpath))
        self.sftp.get(remotepath, localpath, callback=view)

    def close(self):
        self.sftp.close()
        self.transport.close()

    def run(self):
        self.service_test()

    def service_test(self):
        print('b')
        for i in range(self.ip):
            print(i)
            time.sleep(0.2)
        print('e')
        pass


def view(transferred, full_size):

    print('Transferred:{}/{}\r'.format(transferred, full_size))


def main():
    print('test begin')
    t = [TestThread(5) for _ in range(3)]
    for i in t:
        i.start()
    for i in t:
        i.join()
    print('test end')


if __name__ == '__main__':
    # main()
    t = TestThread('172.27.1.1')
    t.file_download()
    t.close()
    pass
