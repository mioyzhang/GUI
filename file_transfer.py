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
import tqdm
import socket
import argparse


PORT = 1234
BUFFER_SIZE = 1024


def udp_send(file_path, ip, port=PORT):
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    file_name = file_path.split('/')[-1]
    file_size = os.path.getsize(file_path)

    sock_s.connect((ip, port))
    # sock_s.send(f'{file_name} {file_size}'.encode())
    sock_s.send('{} {}'.format(file_name, file_size).encode())

    print('send {} to {}:{}'.format(file_name, ip, PORT))
    progress = tqdm.tqdm(total=file_size, unit='B', unit_divisor=1024)

    with open(file_path, 'rb') as f:
        while True:
            buf = f.read(BUFFER_SIZE)
            if not buf:
                progress.close()
                print('传输完成')
                sock_s.sendall('EOF'.encode())
                break

            progress.update(len(buf))
            sock_s.sendall(buf)
    sock_s.close()


def udp_recv(port=PORT):
    print('looking at port {}'.format(port))

    sock_r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_r.bind(('0.0.0.0', port))

    data, address = sock_r.recvfrom(2048)
    file_name, file_size = data.decode().split()
    file_size = int(file_size)
    print('recv {} from {}'.format(file_name, address))
    progress = tqdm.tqdm(total=file_size, unit='B', unit_divisor=1024)

    with open(file_name, 'wb') as f:
        while True:
            data, address = sock_r.recvfrom(BUFFER_SIZE)
            if data == b'EOF':
                progress.close()
                print('传输完成')
                break
            progress.update(len(data))
            f.write(data)
    sock_r.close()


def tcp_recv(port=PORT):
    # service
    sock = socket.socket()
    sock.bind(('0.0.0.0', port))
    sock.listen(5)

    while True:
        cnt, addr = sock.accept()
        print('connect from {}'.format(addr))

        data = cnt.recv(BUFFER_SIZE)
        file_name, file_size = data.decode().split()
        file_size = int(file_size)
        print('recv {} from {}'.format(file_name, addr))
        progress = tqdm.tqdm(total=file_size, unit='B', unit_divisor=1024)

        with open(file_name, 'wb') as f:
            while True:
                data = cnt.recv(BUFFER_SIZE)
                if data:
                    progress.update(len(data))
                    f.write(data)
                else:
                    progress.close()
                    print('传输完成')
                    break
        cnt.close()


def tcp_send(file_path, ip, port=PORT):
    # client
    file_name = file_path.split('/')[-1]
    file_size = os.path.getsize(file_path)

    sock = socket.socket()
    sock.connect((ip, port))
    print('connect to {}:{}'.format(ip, port))

    print('send {} to {}:{}'.format(file_name, ip, PORT))
    sock.send('{} {}'.format(file_name, file_size).encode())
    progress = tqdm.tqdm(total=file_size, unit='B', unit_divisor=1024)

    with open(file_path, 'rb') as f:
        while True:
            buf = f.read(BUFFER_SIZE)
            if not buf:
                progress.close()
                print('传输完成')
                break

            progress.update(len(buf))
            sock.sendall(buf)

    sock.close()


def test():
    file_size = os.path.getsize(path)
    print(file_size)
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--send', type=str, help='Send')
    group.add_argument('-r', '--recv', action='store_true', help='Recv')

    parser.add_argument('-p', '--protocol', type=str, default='UDP', choices=['UDP, TCP'],
                        help='Use UDP/UDP transfer protocol')
    parser.add_argument('-f', '--file', type=str, help=' transfer file')
    args = parser.parse_args()

    path = '/root/pypj/myplot2.png'

    # if args.send:
    #     send_udp(path, args.send)
    #
    # if args.recv:
    #     recv_udp()

    if args.send:
        tcp_send(path, args.send)

    if args.recv:
        tcp_recv()
