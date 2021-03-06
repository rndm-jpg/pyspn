import numpy as np
import torch
import pdb
import math
from .leaf import *
from collections import defaultdict, deque

class Structure(object):
    def __init__(self):
        self.roots = []
        self.weights = []

    def print_level_stat(self, level, level_type, level_nodes, edge_count):
        print("Level " + str(level) + " (" + level_type + ") : " + str(len(level_nodes)) + " nodes, " + str(edge_count) + " edges")

    def print_level_weight_indices(self, level, level_type, level_nodes, edge_count):
        if level_type != "Sum":
            return

        str_by_nodes = []
        for node in level_nodes:
            node_idx = list(node.weight_id_by_child.values())
            str_by_nodes.append( str(node_idx) )

        level_node_str = ''.join(str_by_nodes)

        print(level_node_str)

    def print_stat(self):
        self.traverse_by_level(self.print_level_stat)

    def print_weight_indices(self):
        self.traverse_by_level(self.print_level_weight_indices)

    def traverse_by_level(self, fn):
        '''
        :param fn: takes in #level, level type, nodes, edge_count
        :return:
        '''
        q = deque(self.roots)

        level = 0
        total_nodes = 0
        total_edges = 0
        visited = {}

        while q:
            level_size = len(q)
            node_count = 0
            edge_count = 0

            level_type = None
            level_nodes = []
            while level_size:
                u = q.popleft()
                level_nodes.append(u)
                level_size -= 1

                level_type = u.node_type

                node_count += 1

                if isinstance(u,PixelLeaf):
                    continue

                edge_count += len(u.edges)

                for e in u.edges:
                    v = e.child
                    if v in visited:
                        continue

                    q.append(v)
                    visited[v] = True

            total_nodes += node_count
            total_edges += edge_count

            fn(level, level_type, level_nodes, edge_count)

            level += 1
