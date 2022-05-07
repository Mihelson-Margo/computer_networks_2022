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


def send_package(dest_addr, ttl, timeout=1):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                              socket.getprotobyname('icmp'))
    my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

    packet_id = random.randint(1, (1 << 16)-1);
    packet = create_packet(packet_id)
    sent = my_socket.sendto(packet, (dest_addr, 1))
    result = receive_package(my_socket, packet_id, time.time(), timeout)
    my_socket.close()
    return result


def receive_package(my_socket, packet_id, time_sent, timeout):
    time_left = timeout
    while True:
        ready = select.select([my_socket], [], [], time_left)
        if ready[0] == []:
            return
        time_received = time.time()
        packet, (addr, _) = my_socket.recvfrom(1024)
        icmp_header = packet[20:28]
        icmp_type, code, checksum, p_id, sequence = struct.unpack(
            'bbHHh', icmp_header)
        if p_id == packet_id or (icmp_type == 11 and code == 0):
            return time_received - time_sent, addr, p_id == packet_id
        time_left -= time_received - time_sent
        if time_left <= 0:
            return


def trace(addr, n=3, timeout=1):
    ttl = 0
    flag = 0
    while not flag:
        ttl += 1
        for i in range(n):
            res = send_package(addr, ttl, timeout=timeout)
            if res:
                delay, resp_addr, cur_flag = res
                flag |= cur_flag
                try:
                    hostname, _, _ = socket.gethostbyaddr(resp_addr)
                except Exception:
                    hostname = 'Unknown'
                print(f'RTT = {delay*100 :.2f} ms, {resp_addr} {hostname}')
            else:
                print('***')
            time.sleep(timeout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', type=str)
    parser.add_argument('n', type=int)
    args = parser.parse_args()
    trace(args.addr, args.n)

