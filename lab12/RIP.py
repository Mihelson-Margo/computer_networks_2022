import numpy as np
import random
import threading
import time

my_lock = threading.Lock()

class Node:
    def __init__(self, idx, ip, neighbours, n, simulation_cycles):
        self.neighbours = neighbours
        self.idx = idx
        self.ip = ip
        self.n = n
        self.simulation_cycles = simulation_cycles

        self.dist = np.zeros(n, dtype=int)
        self.next_id = n * [-1]
        for i in range(n):
            if i != idx:
                self.dist[i] = 10000

        for v_idx in self.neighbours:
            self.dist[v_idx] = 1
            self.next_id[v_idx] = v_idx

    def update(self, sender_id, graph):
        for v_idx in range(self.n):
            if self.dist[v_idx] > graph[sender_id].dist[v_idx] + 1:
                self.dist[v_idx] = graph[sender_id].dist[v_idx] + 1
                self.next_id[v_idx] = sender_id

    def print_routing(self, graph):
        print(f"{'Source IP':20}{'Destination IP':20}{'Next Hop':20}{'Metric':10}")
        for idx in range(self.n):
            if self.next_id[idx] == -1:
                next_ip = '0.0.0.0'
            else:
                next_ip = graph[self.next_id[idx]].ip
            print(f"{self.ip:20}{graph[idx].ip:20}{next_ip:20}{self.dist[idx]:10}")
        print()

    def simulate(self, graph, lock):
        for i in range(self.simulation_cycles):
            with lock:
                print(f"Simulations step {i+1} of router {self.ip}:")
                self.print_routing(graph)
            for u_idx in self.neighbours:
                with lock:
                    graph[u_idx].update(self.idx, graph)
            time.sleep(1)


def generate_ip(k):
    a = random.randint(1, 254)
    b = random.randint(1, 254)
    c = random.randint(1, 254)
    return f"{a}.{b}.{c}.{k}"


def generate_graph(n = 6):
    neighbours = {}
    ips = []
    for i in range(n):
        neighbours[i] = []
        ips.append(generate_ip(i+1))

    print("The network has following links between routers:")
    for i in range(n):
        for j in range(i+1, n):
            if random.randint(1, 100) < 33:
                neighbours[i].append(j)
                neighbours[j].append(i)
                print(f"{ips[i]} <-> {ips[j]}")
    print()

    graph = []
    for i in range(n):
        graph.append(Node(i, ips[i], neighbours[i], n, 3))

    return graph


def simulate_all(graph):
    threads = []
    lock = threading.Lock()
    for idx, node in enumerate(graph):
        th = threading.Thread(target=node.simulate, args=(graph, lock,))
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

    for node in graph:
        print(f"Final state of router {node.ip} table:")
        node.print_routing(graph)


def main():
    graph = generate_graph()

    simulate_all(graph)


if __name__ == '__main__':
    main()
