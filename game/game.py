import pygame
import random

from simulation.generate_graph import SimulationGraph
from simulation.simulator import Simulator

class Game:
    def __init__(self):
        pygame.init()
        self.text_large = pygame.font.Font('./fonts/OpenSans.ttf', 50)
        self.text_small = pygame.font.Font('./fonts/OpenSans.ttf', 20)
        self.screen = pygame.display.set_mode((1920, 1080))
        self.done = False
        self.clock = pygame.time.Clock()
        self.size_square = 20
        self.node_selected = False
        self.connections = []
        self.round = 1500
        self.current_node = 0
        self._create_objects()
        self._define_neighbors()
        # self._create_connections()
        self._create_simulation()

    def _create_simulation(self):
        sg = SimulationGraph(self.nodes, 1)
        self.simulator = Simulator(sg)


    def _create_objects(self):
        self.brasil = pygame.image.load('Pictures/mapa_brasil.png')
        self.nodes = {}
        self._create_tribes()
        self.next_button = {'object': pygame.Rect(1600, 850, 300, 150),
                            'color': (255, 255, 255), 'is_clicked': False}

    def _create_node(self, x, y, color, name, nationality):
            pygame_obj = pygame.Rect(x, y, self.size_square, self.size_square)
            pop = random.randint(40, 200) if nationality == 'native' \
                  else random.randint(20, 50)
            result = {
                'object': pygame_obj,
                'color': color,
                'name': name,
                'population': pop,
                'number': self.current_node,
                'nationality': nationality,
            }
            self.current_node += 1
            return result

    def _create_tribes(self):
        self.nodes['tupi_2'] = self._create_node(1200, 310, (255, 0, 0), 'Tupi', 'native')
        self.nodes['tupi_1'] = self._create_node(700, 330, (255, 0, 0), 'Tupi', 'native')
        self.nodes['tupi_3'] = self._create_node(800, 600, (255, 0, 0), 'Tupi', 'native')
        self.nodes['tupi_4'] = self._create_node(700, 300, (255, 0, 0), 'Tupi', 'native')
        self.nodes['je'] = self._create_node(950, 400, (255, 0, 0), 'Je', 'native')
        self.nodes['je_2'] = self._create_node(900, 700, (255, 0, 0), 'Je', 'native')
        self.nodes['karib'] = self._create_node(700, 150, (255, 0, 0), 'Karib', 'native')
        self.nodes['pano'] = self._create_node(400, 300, (255, 0, 0), 'Pano', 'native')
        self.nodes['charrua'] = self._create_node(800, 900, (255, 0, 0), 'Charrua', 'native')
        self.nodes['aruak'] = self._create_node(500, 250, (255, 0, 0), 'Aruak', 'native')
        self.nodes['tukano'] = self._create_node(550, 175, (255, 0, 0), 'Tukano', 'native')
        self.nodes['surui'] = self._create_node(600, 400, (255,0,0), 'Surui', 'native')
        self.nodes['araute'] = self._create_node(900, 340, (255, 0, 0), 'Araute', 'native')
        self.nodes['pataxo'] = self._create_node(1100, 550, (255, 0, 0), 'Pataxo', 'native')
        self.nodes['portugues'] = self._create_node(1160, 500, (0, 0, 255), 'Portugues', 'portuguese')

    def _draw_info_board(self):
        self.close = pygame.Rect(1700, 650, 150, 50)
        if (self.node_selected != False):
            node = self.node_selected
            board = pygame.Rect(1400, 20, 500, 700)
            pygame.draw.rect(self.screen, [255, 255, 255], board)

            pygame.draw.rect(self.screen, [200, 200, 200], self.close)

            close_text = self.text_small.render("Fechar", False, (0, 0, 0))
            self.screen.blit(close_text, (1745, 655))


            node_name = self.text_large.render(self.nodes[node]['name'], False,
                                               (255, 0, 0))
            self.screen.blit(node_name, (1420, 20))

            population = self.text_small.render("Populacao: {}".format(
                self.simulator.g.node[self.nodes[node]['number']]['population']),
                False, (255, 0, 0)
            )
            self.screen.blit(population, (1420, 150))

            domination = self.text_small.render(
                'Nacionalidade dominante: {}'.format('Português' if self.simulator\
                .g.node[self.nodes[node]['number']]['nationality'] == 'portuguese'\
                else 'Nativo'), False, (255, 0, 0))
            self.screen.blit(domination, (1420, 240))

            # number = self.text_small.render("Numero: {}".format(self.nodes[node]['number']), False, (255, 0, 0))
            # self.screen.blit(number, (1420, 200))

    def _draw_next_round_button(self):
        color = self.next_button['color']
        if (self.next_button['is_clicked']):
            color = (255, 0, 255)
        pygame.draw.rect(self.screen, color, self.next_button['object'])
        next_txt = self.text_large.render("NEXT", False, (0, 0, 0))
        self.screen.blit(next_txt,(1680, 880))

    def _draw_connections(self):
        # for i in self.connections:
        #     if (i['is_positive']):
        #         color = (0, 0, 255)
        #     else:
        #         color = (255, 0 ,0)
        #     pygame.draw.line(self.screen, color, i['node_1'],  i['node_2'], 1)
        for n, m in self.simulator.g.edges():
            pygame.draw.line(
                self.screen,
                (0, 0, 255) if self.simulator.g.edges[n, m]['label'] == '+' else (255, 0, 0),
                self._gen_pos(self._get_node_by_number(n)),
                self._gen_pos(self._get_node_by_number(m)), 1)

    def _define_neighbors(self):
            self.nodes['tupi_1']['neighbors'] = [3, 11, 12, 9, 10, 6]
            self.nodes['tupi_2']['neighbors'] = [12, 4, 13]
            self.nodes['tupi_3']['neighbors'] = [5, 8, 4, 13]
            self.nodes['tupi_4']['neighbors'] = [1, 11, 9, 10, 6]
            self.nodes['je']['neighbors'] = [12, 0, 13, 2]
            self.nodes['je_2']['neighbors'] = [2, 8, 13]
            self.nodes['karib']['neighbors'] = [10, 9, 3, 12]
            self.nodes['pano']['neighbors'] = [9, 11, 10]
            self.nodes['charrua']['neighbors'] = [5, 2]
            self.nodes['aruak']['neighbors'] = [7, 10, 11, 3, 1]
            self.nodes['tukano']['neighbors'] = [9, 3, 6]
            self.nodes['surui']['neighbors'] = [7, 1, 9, 3]
            self.nodes['araute']['neighbors'] = [4, 1, 3, 0]
            self.nodes['pataxo']['neighbors'] = [4, 5, 0]
            self.nodes['portugues']['neighbors'] = [0, 13]

    def _get_node_by_number(self, number):
        for i in self.nodes:
            if (self.nodes[i]['number'] == number):
                return i

    def _check_nodes_connected(self, node_1, node_2):
        for i in self.connections:
            if (i['nodes_connected'] == (node_1, node_2) or i['nodes_connected'] == (node_2, node_1)):
                return True
        return False

    def _gen_pos(self, n):
        delta = self.size_square / 2
        return (self.nodes[n]['object'].left + delta,
                self.nodes[n]['object'].top + delta)

    def _create_connections(self):
        delta = self.size_square / 2
        for i in self.nodes:
            for j in self.nodes[i]['neighbors']:
                node_1 = self._get_node_by_number(j)
                node_2 = i
                is_positive = random.choice([True, False])
                if (not self._check_nodes_connected(node_1, node_2)):
                    pos_1 = (self.nodes[node_1]['object'].left + delta,
                             self.nodes[node_1]['object'].top + delta)
                    pos_2 = (self.nodes[node_2]['object'].left + delta,
                             self.nodes[node_2]['object'].top + delta)
                    connection = {'node_1': pos_1, 'node_2': pos_2,
                                  'is_positive': is_positive, 'nodes_connected': (node_1, node_2)}
                    self.connections.append(connection)

    def _draw_text(self):
        round_num = self.text_large.render(str(self.round), False, (255, 255, 255))
        self.screen.blit(round_num, (10, 10))

    def run_game(self):
        # Main Loop
        while not self.done:
            # Eventos
            for event in pygame.event.get():
                # Quit
                if event.type == pygame.QUIT:
                    self.done = True
                # Press Mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Loop para clicar nas tribos
                    for i in self.nodes:
                        if self.nodes[i]['object'].collidepoint(mouse_pos):
                            self.node_selected = i
                    # Clicar no Next
                    if self.next_button['object'].collidepoint(mouse_pos):
                        self.next_button['is_clicked'] = True
                        self.round += 10
                        self.simulator.iteration()  # next iteration
                    # Clicar no fechar
                    if self.close.collidepoint(mouse_pos):
                        self.node_selected = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.next_button['is_clicked'] = False

            # Tela Preta e Mapa do Brasil
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.brasil, (300, 0))

            # Cor dos nós
            for i in self.nodes:
                if (i == self.node_selected):
                    self.nodes[i]['color'] = (0, 255 ,0)
                else:
                    self.nodes[i]['color'] = (255, 0, 0) if \
                                             self.simulator.g.nodes[
                                                 self.nodes[i]['number']]['nationality'] == 'native'\
                                             else (0, 0, 255)
                pygame.draw.rect(self.screen, self.nodes[i]['color'], self.nodes[i]['object'])

            # Funcoes de draw extras
            self._draw_info_board()
            self._draw_connections()
            self._draw_next_round_button()
            self._draw_text()
            pygame.display.flip()
            self.clock.tick(60)
