import numpy as np

class Node:
    def __init__(self, idx, neighbours, n):
        self.neighbours = neighbours
        self.idx = idx
        self.n = n
        self.d = np.zeros(n)
        for i in range(n):
            if i != idx:
                self.d[i] = np.inf

    def update(self, graph):
        new_dists = self.d.copy()
        for v_idx, v_c in self.neighbours:
            for i in range(self.n):
                new_dists[i] = min(new_dists[i], v_c + graph[v_idx].d[i])

        if np.sum(new_dists != self.d) > 0:
            self.d = new_dists
            return [v_idx for v_idx, _ in self.neighbours]
        else:
            return []


def calc_dists(graph, start_v):
    queue = [start_v]
    while len(queue) > 0:
        cur_node = queue[0]
        queue = queue[1:]
        idxs = graph[cur_node].update(graph)
        for node_idx in idxs:
            if node_idx not in queue:
                queue.append(node_idx)

    return graph


def build_graph():
    n = 4
    neighbours = {}
    neighbours[0] = [(1, 1), (2, 3), (3, 7)]
    neighbours[1] = [(0, 1), (2, 1)]
    neighbours[2] = [(0, 3), (1, 1), (3, 2)]
    neighbours[3] = [(0, 7), (2, 2)]

    graph = []
    for i in range(n):
        graph.append(Node(i, neighbours[i], n))

    dists = np.array([[0, 1, 2, 4],
                      [1, 0, 1, 3],
                      [2, 1, 0, 2],
                      [4, 3, 2, 0]])
    return graph, dists


def change_edge(graph):
    # change weight of edge 0 <-> 3 from 7 to 1
    graph[0].neighbours[2] = (3, 1)
    graph[3].neighbours[0] = (0, 1)
    dists = np.array([[0, 1, 2, 1],
                      [1, 0, 1, 2],
                      [2, 1, 0, 2],
                      [1, 2, 2, 0]])
    return graph, dists


def main():
    graph, true_dists = build_graph()

    for _ in range(2):
        graph = calc_dists(graph, 0)

        for idx, node in enumerate(graph):
            assert(np.sum(true_dists[idx, :] != node.d) == 0)
            print(node.d)
        print("")

        graph, true_dists = change_edge(graph)


if __name__ == '__main__':
    main()
