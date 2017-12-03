import pickle

from random import choice, randint, random
from functools import reduce
from random_graph import *


class Simulator:

    PORTUGUESE = 'portuguese'
    NATIVE = 'native'


    def __init__(self, g_obj):
        self.g = g_obj.g
        self.g_obj = g_obj
        self.moves = []


    def _count_pt_neighbors(self, n):
        return sum(list(map(lambda x: x[1],
                            filter(lambda x: x[0]['nationality'] == self.PORTUGUESE,
                                map(lambda x: (self.g.node[x], 1),
                                    list(self.g.neighbors(n)))))))


    def _fight_native_vs_native(self, n, m):
        '''
        returns the looser of a battle between natives;
        takes into consideration having portuguese neighbors
        as an advantage
        '''
        pt0 = self._count_pt_neighbors(n)
        pt1 = self._count_pt_neighbors(m)
        if pt0 == pt1:
            return n if choice([pt0, pt1]) == pt1 else m
        elif pt0 > pt1:
            return m
        return n


    def _portuguese_vs_native(self, n, m):
        '''
        returns true if the first one is pt and the second
        one is a native
        '''
        return self.g.node[n]['nationality'] == self.PORTUGUESE and \
            self.g.node[m]['nationality'] == self.NATIVE


    def _fight(self, n, m):
        '''
        returns the looser of a simulated fight between n and m
        '''
        P = 70  # 70% chance
        if self.g.node[n]['nationality'] == self.g.node[m]['nationality'] and \
           self.g.node[n]['nationality'] == self.NATIVE:
            return self._fight_native_vs_native(n, m)
        elif self.g.node[n]['nationality'] == self.g.node[m]['nationality'] and \
             self.g.node[n]['nationality'] == self.PORTUGUESE:
            return choice([n, m])
        elif self._portuguese_vs_native(n, m):
            return m if randint(1, 100) > P else n
        elif self._portuguese_vs_native(m, n):
            return n if randint(1, 100) > P else m
        return -1  # error


    def _flip_edge(self, n, m):
        e = self.g.edges[n, m]['label']
        self.g.edges[n, m]['label'] = '-' if e == '+' else '+'


    def _resolve_combat(self, fighters):
        for l, w in fighters:
            # winner splits population, looser dies ;-;
            pop = self.g.node[w]['population'] // 2
            self.g.node[w]['population'] -= pop
            self.g.node[l]['population'] = pop
            self.g.node[l]['nationality'] = self.g.node[w]['nationality']  # converted

            for n in list(self.g.neighbors(l)):
                self._flip_edge(l, n)


    def _save_moves(self):
        self.moves.append({
            'nodes': [{
                'number': n,
                'population': self.g.node[n]['population'],
                'nationality': self.g.node[n]['nationality'],
            } for n in g.nodes()],
            'edges': [{
                'nodes': (n, m),
                'label': g.edges[n, m]['label'],
            } for n, m in g.edges()],
            'initial_population': self.g.initial_population
        })


    def save_game(self, fname):
        ''' fname str: like "game00.p" '''
        pickle.dump(self.moves, open(fname, 'wb'))


    def iteration(self):
        P = .1  # 10% chance an edge will fight
        fighters = set()
        for n, m in self.g.edges():
            if self.g.edges[n, m]['label'] == '-' and random() < P:
                l = self._fight(n, m)
                fighters.add((l, m if l == n else n))  # (looser, winner)

        self._resolve_combat(fighters)
        self._save_moves()


    def simulate(self, n):
        for _ in range(n):
            self.iteration()

        self.show_results()

    def show_results(self):
        pt = 0
        nt = 0

        for n in self.g.nodes():
            if self.g.node[n]['nationality'] == self.PORTUGUESE:
                pt += self.g.node[n]['population']
            else:
                nt += self.g.node[n]['population']

        try:
            print('''
            portuguese: {:6d} -- {:3.2f}% of total -- {:3.2f}% of initial
            native:     {:6d} -- {:3.2f}% of total -- {:3.2f}% of initial
            '''.format(pt, (pt / (pt + nt)) * 100,
                    pt / self.g_obj.initial_population['portuguese'] * 100,
                    nt, (nt / (pt + nt)) * 100,
                    nt / self.g_obj.initial_population['native'] * 100))
        except:  # division by 0
            print('Both populations are 0')


if __name__ == '__main__':
    gobj = RandomGraph(500, .2)
    gobj.generate_graph()
    gobj.generate_edges(.05)
    sim = Simulator(gobj)
    sim.simulate(5)
