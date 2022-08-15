#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Project : pypj
# @File    : file_transfer.py
# @IDE     : PyCharm
# @Author  : zhang bin
# @Date    : 2022/8/15 15:00:03
# @DES     : 
"""
import os
import time
# import tqdm
import socket
import argparse


PORT = 1234


def send_udp(file_path, ip, port=PORT):
    print('send pkg to {}:{}'.format(ip, PORT))
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # filesize = os
    file_name = file_path.split('/')[-1]
    file_size = os.path.getsize(file_path)

    buffer_size = 2048

    sock_s.connect((ip, port))
    sock_s.send(f'{file_name} {file_size}'.encode())

    with open(file_path, 'rb') as f:
        while True:
            buf = f.read(buffer_size)
            if not buf:
                print('传输完成')
                sock_s.sendall('EOF'.encode())
                break

            sock_s.sendall(buf)

    sock_s.close()


def recv_udp(port=PORT):
    print('looking at port {}'.format(port))

    buffer_size = 2048

    sock_r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_r.bind(('0.0.0.0', port))

    data, address = sock_r.recvfrom(buffer_size)
    print(address)
    print(data.decode())


    while True:
        data, address = sock_r.recvfrom(buffer_size)
        print(len(data))
        print()

    pass


def test():
    file_size = os.path.getsize(path)
    print(file_size)
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--send', action='store_true', help='Send')
    group.add_argument('-r', '--recv', action='store_true', help='Recv')

    parser.add_argument('-p', '--protocol', type=str, default='UDP', choices=['UDP, TCP'],
                        help='Use UDP/UDP transfer protocol')
    parser.add_argument('-f', '--file', type=str, help=' transfer file')
    args = parser.parse_args()

    if args.protocol == 'UDP':
        pass

    path = '/root/pypj/myplot2.png'
    if args.send:
        send_udp(path, '127.0.0.1')

    if args.recv:
        recv_udp()
