import sys
sys.path.append('..')

import numpy as np
import socnet as sn

from random import randint, choice


class RandomGraph:

    def __init__(self, total_nodes, percentage_portuguese):
        self.total_nodes = total_nodes
        self.percentage_portuguese = percentage_portuguese
        self.percentage_native = 1 - percentage_portuguese


    def generate_graph(self):
        self.g = sn.generate_empty_graph(self.total_nodes)
