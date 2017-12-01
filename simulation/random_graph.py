import sys
sys.path.append('..')

import numpy as np
import socnet as sn

from random import randint, choice, random


class RandomGraph:

    def __init__(self, total_nodes, percentage_portuguese):
        self.total_nodes = total_nodes
        self.percentage_portuguese = percentage_portuguese
        self.percentage_native = 1 - percentage_portuguese
        self.initial_population = None
        self.g = None


    def generate_graph(self):
        self.g = sn.generate_empty_graph(self.total_nodes)
        self.initial_population = {
            'portuguese': 0,
            'native': 0
        }

        for n in range(int(self.total_nodes * self.percentage_portuguese)):
            self.g.node[n]['nationality'] = 'portuguese'
            self.g.node[n]['color'] = (255,255,0)
            self.g.node[n]['label'] = n
            pop = randint(20, 50)
            self.g.node[n]['population'] = pop
            self.initial_population['portuguese'] += pop

        for n in range(int(self.total_nodes * self.percentage_portuguese),
                       self.total_nodes):
            self.g.node[n]['nationality'] = 'native'
            self.g.node[n]['color'] = (255,0,255)
            self.g.node[n]['label'] = n
            pop = randint(40, 200)
            self.g.node[n]['population'] = pop
            self.initial_population['native'] += pop


    def generate_edges(self, P):
        '''
        :P  -> Float between 0 and 1
        '''
        for n in self.g.nodes():
            for i in self.g.nodes():
                if n != i and random() < P:
                    self.g.add_edge(n,i)
                    self.g.edges[(n, i)]['label'] = choice(['+', '-'])
