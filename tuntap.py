import sys
import time
import dpkt
import socket
import argparse
import threading
from pytun import TunTapDevice


# sys.path.append('/home/3yuan')

threadLock = threading.Lock()
PORT = 1234


def lock(func):
    def wrapper(*args, **kwargs):
        threadLock.acquire()
        func(*args, **kwargs)
        threadLock.release()
    return wrapper


@lock
def display_packet(packet):
    for i in range(len(packet)):
        print('%02X ' % packet[i], end='')
        if (i + 1) % 16 == 0:
            print()
        elif (i + 1) % 8 == 0:
            print(' ', end='')
    print('\n')


def tun_create(tun_addr):
    tun_tap = TunTapDevice(name='tun0')
    tun_tap.addr = tun_addr
    tun_tap.netmask = '255.255.255.0'
    tun_tap.mtu = 200
    tun_tap.up()
    return tun_tap


def tun_send():
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('looking at tun0...')
    while True:
        buf = tun.read(tun.mtu)
        if not buf:
            continue

        try:
            sock_s.sendto(buf, (remote_ip, PORT))
            # print(f'send: {len(buf)}')
            display_packet(buf)
        except BaseException as e:
            print('send pkt to {}:{} error'.format(remote_ip, PORT))
            print(e)


def tun_recv():
    try:
        sock_r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_r.bind(('0.0.0.0', PORT))
    except BaseException as e:
        print(e)
    else:
        print('listen on {}:{}...'.format('0.0.0.0', PORT))

        while True:
            data, address = sock_r.recvfrom(2048)
            # tun.write(tun_header + data)
            tun.write(data)
            # print(f'recv: {len(data)}')
            display_packet(data)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument('-s', '--send', type=str, help='send pkg to')
    parser.add_argument('-n', '--node', choices=['n1', 'n2'])
    arg = parser.parse_args()

    node = arg.node
    if arg.node == 'n1':
        tun_ip, remote_ip = '172.0.0.1', '10.0.0.2'
    else:
        tun_ip, remote_ip = '172.0.0.2', '10.0.0.1'

    tun = tun_create(tun_ip)

    threads = [
        threading.Thread(target=tun_send),
        threading.Thread(target=tun_recv),
    ]
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
