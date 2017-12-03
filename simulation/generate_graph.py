import sys
sys.path.append('..')

import numpy as np
import socnet as sn
import networkx as nx

from random import random, choice, randint


class SGraph:

    def __init__(self):
        self.nodes = None
        self.initial_population = None
        self.g = None
        self.edge_probability = -1.0  # error handling for loaded graphs


class LoadGraph(SGraph):

    def _add_nodes(self, nodes):
        for n in nodes:
            self.g.add_node(
                n['number'],
                nationality=n['nationality'],
                population=n['population']
            )


    def _add_edges(self, edges):
        for e in edges:
            self.g.add_edge(n, m, label=e['label'])


    def _gen_nodes_dic(self):
        self.nodes = [{
            'number': n,
            'neighbors': [(m, True if self.g.edges[n, m]['label'] == '+' else False)
                          for m in list(self.g.neighbors())],
            'nationality': self.g.node[n]['nationality'],
        } for n in g.nodes()]


    def __init__(self, fname):
        ''' fname str: file name like "game00.p" '''
        state = None
        try:
            state = pickle.load(open(fname, 'rb'))
        except IOError as e:
            print('could not find file with name {}'.format(fname))
            return

        self.g = nx.Graph()
        self._add_nodes(state['nodes'])
        self._add_edges(state['edges'])
        self._gen_nodes_dic()
        self.initial_population = state['initial_population']


class SimulationGraph(SGraph):

    def __init__(self, nodes, p):
        '''
        :nodes => nodes['number']      # id
               => nodes['neighbors']   # neighbors (id, bool(pos/neg))
               => nodes['nationality]  # str (portuguese/native)
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
                    self.g.add_edge(n, m[0], label='+' if m[1] else '-')


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
