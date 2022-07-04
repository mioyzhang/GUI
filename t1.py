#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Project : pypj
# @File    : multi_service_test.py
# @IDE     : PyCharm
# @Author  : zhang bin
# @Date    : 2022/7/4 15:24:53
# @DES     : 
"""
import time
import threading
import paramiko


def service_test():
    print('b')
    for i in range(5):
        print(i)
        time.sleep(0.2)
    print('e')
    pass


def test():
    print('test begin')
    p = [threading.Thread(target=service_test) for _ in range(3)]
    for i in p:
        i.start()
    for i in p:
        i.join()
    print('test end')


def view(transferred, toBeTransferred):
    print('Transferred:{}/{}\r'.format(transferred, toBeTransferred))


def file_download(ip):
    transport = paramiko.Transport((ip, 22))
    transport.connect(username='root', password='root')

    sftp = paramiko.SFTPClient.from_transport(transport)
    remotepath = '/home/dell/2019-05-28-15-36-07.dat'
    localpath = '1.txt'
    sftp.get(remotepath, localpath, callback=view)

    sftp.close()
    transport.close()


if __name__ == '__main__':
    # test()
    file_download('172.27.1.1')
    pass
