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
import math
import argparse
import socket
from threading import Thread, Event


PORT = 1234
ACK_PORT = 1235
BUFFER_SIZE = 1024 * 2
SEPARATOR = '<SEPARATOR>'

positions = []
file_name = []
e = Event()


def send_file(file_path, ip):

    global positions
    global file_name

    address = (ip, PORT)
    file_name.append(file_path.split('/')[-1])
    file_size = os.path.getsize(file_path)

    with open(file_path, 'rb') as f:
        content = f.read()

    positions = [i * BUFFER_SIZE for i in range(int(math.ceil(file_size / BUFFER_SIZE)))]

    e.set()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUFFER_SIZE)

    print('send {}_{}_{}_{}'.format('send', file_name[0], file_size, len(positions)))
    while file_name:
        sock.sendto('{}_{}_{}_{}'.format('send', file_name[0], file_size, len(positions)).encode(), address)
        time.sleep(0.1)

    while positions:
        for pos in positions:
            sock.sendto('{}_'.format(pos).encode() + content[pos:pos + BUFFER_SIZE], address)

        time.sleep(0.1)


def recv_ack():
    global file_name
    global positions

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', ACK_PORT))

    e.clear()
    e.wait()

    while file_name:
        date, _ = sock.recvfrom(1024)
        f = date.decode().split('_')[0]
        print('recv {} ack'.format(f))
        if f in file_name:
            file_name.remove(f)

    while positions:
        date, _ = sock.recvfrom(1024)
        pos = int(date.decode().split('_')[0])
        if pos in positions:
            positions.remove(pos)

        print('recv {} ack, left {}'.format(pos, len(positions)))


def send(file_path, ip):
    t1 = Thread(target=send_file, args=(file_path, ip))
    t2 = Thread(target=recv_ack)

    t2.start()
    t1.start()

    t1.join()
    t2.join()


def recv():
    print('looking at port {}'.format(PORT))

    sock_r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_r.bind(('0.0.0.0', PORT))

    sock_ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    recv_file_name = None
    pos_len = math.inf
    buf = dict()

    while True:
        data, address = sock_r.recvfrom(BUFFER_SIZE)
        ack_address = (address[0], ACK_PORT)

        if data.startswith(b'send_'):
            if not recv_file_name:
                _, recv_file_name, file_size, pos_len = data.decode().split('_')
                print('recv {} from {}'.format(recv_file_name, address))
                sock_ack.sendto('{}_ack'.format(recv_file_name).encode(), ack_address)
                print('send {}_ack to {}'.format(recv_file_name, ack_address))

            continue

        pos, data = data.split(b'_', maxsplit=1)
        pos = int(pos.decode())

        if pos not in buf.keys():
            buf[pos] = data

        sock_ack.sendto('{}_ack'.format(pos).encode(), ack_address)

        print('recv {}, total {}'.format(pos, len(buf.items())))

        if len(buf.keys()) == pos_len:
            break

    sock_r.close()
    sock_ack.close()

    p = sorted(buf.keys())
    with open(recv_file_name, 'wb') as f:
        for i in p:
            f.write(buf[i])


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

    if args.send:
        send(path, args.send)

    if args.recv:
        recv()
