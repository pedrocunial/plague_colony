import sys
sys.path.append('..')

import numpy as np
import socnet as sn
import networkx as nx

from random import random, choice, randint


class SimulationGraph:



    def __init__(self, nodes, p):
        '''
        :nodes => nodes['number']      # id
               => nodes['neighbors']   # neighbors ids
        :p     => float between 0 and 1
        '''
        self.nodes = nodes
        self.generate_nodes()
        self.generate_edges(p)
        self.edge_probability = p


    def generate_edges(self, p):
        for n in self.nodes:
            for m in n['neighbors']:
                if random() < P:  # chance to fight
                    self.g.add_edge(n, m)


    def generate_nodes(self):
        self.g = nx.Graph()
        self.initial_population = {
            'portuguese': 0,
            'native': 0,
        }
        for n in self.nodes:
            pop = randint(40, 200)
            self.initial_population['native'] += pop
            self.g.add_node(
                n['number'],
                nationality='native',
                population=pop
            )
