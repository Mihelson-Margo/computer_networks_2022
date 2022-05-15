import numpy as np
import random


class Node:
    def __init__(self, idx, ip, neighbours, n):
        self.neighbours = neighbours
        self.idx = idx
        self.ip = ip
        self.n = n
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


def generate_ip(k):
    a = random.randint(1, 254)
    b = random.randint(1, 254)
    c = random.randint(1, 254)
    return f"{a}.{b}.{c}.{k}"


def generate_graph(n = 4, _print=True):
    neighbours = {}
    ips = []
    for i in range(n):
        neighbours[i] = []
        ips.append(generate_ip(i+1))

    for i in range(n):
        for j in range(i+1, n):
            if random.randint(1, 100)%2 == 1:
                neighbours[i].append(j)
                neighbours[j].append(i)
                if _print:
                    print(f"{ips[i]} <-> {ips[j]}")

    graph = []
    for i in range(n):
        graph.append(Node(i, ips[i], neighbours[i], n))

    return graph


def simulate(graph, simulation_cycles):
    for i in range(simulation_cycles):
        for v_idx, node in enumerate(graph):
            print(f"Simulations step {i+1} of router {node.ip}:")
            node.print_routing(graph)
            for u_idx in node.neighbours:
                graph[u_idx].update(v_idx, graph)

    for node in graph:
        print(f"Final state of router {node.ip} table:")
        node.print_routing(graph)


def main():
    graph = generate_graph()

    simulate(graph, 3)


if __name__ == '__main__':
    main()
