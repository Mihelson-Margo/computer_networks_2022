import time
import socket
import struct
import select
import random
import argparse


def calc_checksum(bts):
    ones = (1 << 16) - 1
    s = 0
    for i in range((len(bts)+1)//2):
        cur = bts[2*i]
        if 2*i + 1 < len(bts):
            cur += bts[2*i+1] << 8
        s = (s + cur) % (1 << 16)
    return ones ^ s


def checkSum(bts):
    ones = (1 << 16) - 1
    s = 0
    for i in range((len(bts)+1)//2):
        cur = bts[2*i]
        if 2*i + 1 < len(bts):
            cur += bts[2*i+1] << 8
        s = (s + cur) % (1 << 16)
    return s == ones


def create_packet(id):
    data = bytes(str(time.time()), 'utf-8')
    header = struct.pack('bbHHbs', 8, 0, 0, id, 1, data)
    checksum = calc_checksum(header)
    header = struct.pack('bbHHbs', 8, 0, checksum, id, 1, data)
    return header


def send_package(dest_addr, timeout=1):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                              socket.getprotobyname('icmp'))
    packet_id = random.randint(1, (1 << 16)-1);
    packet = create_packet(packet_id)
    sent = my_socket.sendto(packet, (dest_addr, 1))
    delay = receive_ping(my_socket, packet_id, time.time(), timeout)
    my_socket.close()
    return delay


def receive_ping(my_socket, packet_id, time_sent, timeout):
    time_left = timeout
    while True:
        ready = select.select([my_socket], [], [], time_left)
        if ready[0] == []:
            return
        time_received = time.time()
        packet, _ = my_socket.recvfrom(1024)
        icmp_header = packet[20:28]
        icmp_type, code, checksum, p_id, sequence = struct.unpack(
            'bbHHh', icmp_header)
        if p_id == packet_id and checkSum(icmp_header):
            return time_received - time_sent
        time_left -= time_received - time_sent
        if time_left <= 0:
            return


def do_ping(addr, n=5, timeout=1):
    RTTs = []
    n_losts = 0
    for i in range(n):
        delay = send_package(addr, timeout=timeout)
        if delay:
            RTTs.append(delay*100)
            print(f'time = {delay*100 :.2f} ms')
            print(f'rtt min/avg/max = {min(RTTs) :.2f}/{sum(RTTs)/len(RTTs) :.2f}/{max(RTTs) :.2f} ms')
        else:
            n_losts += 1
            print('***')
        print(f'lost {100*n_losts/(i+1) :0.1f}%')
        time.sleep(timeout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', type=str)
    args = parser.parse_args()
    do_ping(args.addr)
