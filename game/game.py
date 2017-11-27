import pygame
import random

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
		self._create_objects()
		self._create_connections()
	
	def _create_objects(self):
		self.brasil = pygame.image.load('Pictures/mapa_brasil.png')
		self.nodes = {}
		self._create_tribes()
		self.next_button = {'object': pygame.Rect(1600, 850, 300, 150), 'color': (255, 255, 255), 'is_clicked': False}	

	def _create_node(self, x, y, color, name):
			pygame_obj = pygame.Rect(x, y, self.size_square, self.size_square)
			result = {'object': pygame_obj, 
								'color': color,
								'name': name,
								'population': str(random.randint(10, 50))
							 }
			return result

	def _create_tribes(self):
		self.nodes['tupi_2'] = self._create_node(1200, 310, [255, 0, 0], 'Tupi')
		self.nodes['tupi_1'] = self._create_node(700, 330, [255, 0, 0], 'Tupi')
		self.nodes['tupi_3'] = self._create_node(800, 600, [255, 0, 0], 'Tupi')
		self.nodes['tupi_4'] = self._create_node(700, 300, [255, 0, 0], 'Tupi')
		self.nodes['je'] = self._create_node(950, 400, [255, 0, 0], 'Je')
		self.nodes['je_2'] = self._create_node(900, 700, [255, 0, 0], 'Je')
		self.nodes['karib'] = self._create_node(700, 150, [255, 0, 0], 'Karib')
		self.nodes['pano'] = self._create_node(400, 300, [255, 0, 0], 'Pano')
		self.nodes['charrua'] = self._create_node(800, 900, [255, 0, 0], 'Charrua')
		self.nodes['aruak'] = self._create_node(500, 250, [255, 0, 0], 'Aruak')
		self.nodes['tukano'] = self._create_node(550, 175, [255, 0, 0], 'Tukano')
		self.nodes['surui'] = self._create_node(600, 400, [255,0,0], 'Surui')
		self.nodes['araute'] = self._create_node(900, 340, [255, 0, 0], 'Araute')
		self.nodes['pataxo'] = self._create_node(1100, 550, [255, 0, 0], 'Pataxo')

	def _draw_info_board(self):
		if (self.node_selected != False):
			node = self.node_selected
			board = pygame.Rect(1400, 20, 500, 700)
			pygame.draw.rect(self.screen, [255, 255, 255], board)

			node_name = self.text_large.render(self.nodes[node]['name'], False, (255, 0, 0))
			self.screen.blit(node_name, (1420, 20))

			population = self.text_small.render("Populacao: {}".format(self.nodes[node]['population']), False, (255, 0, 0))
			self.screen.blit(population, (1420, 150))

	def _draw_next_round_button(self):
		color = self.next_button['color']
		if (self.next_button['is_clicked']):
			color = (255, 0, 255)
		pygame.draw.rect(self.screen, color, self.next_button['object'])
		next_txt = self.text_large.render("NEXT", False, (0, 0, 0))
		self.screen.blit(next_txt,(1680, 880))

	def _draw_connections(self):
		for i in self.connections:
			if (i['is_positive']):
				color = (0, 0, 255)
			else:
				color = (255, 0 ,0)
			pygame.draw.line(self.screen, color, i['node_1'],  i['node_2'], 1)

	def _create_connections(self):
		delta = self.size_square / 2
		for i in range(30):
			node_1 = random.choice(list(self.nodes.keys()))
			node_2 = random.choice(list(self.nodes.keys()))
			is_positive = random.choice([True, False])
			pos_1 = (self.nodes[node_1]['object'].left + delta, self.nodes[node_1]['object'].top + delta)
			pos_2 = (self.nodes[node_2]['object'].left + delta, self.nodes[node_2]['object'].top + delta)
			connection = {'node_1': pos_1, 'node_2': pos_2, 'is_positive': is_positive}
			self.connections.append(connection)

	def _draw_text(self):
		round_num = self.text_large.render(str(self.round), False, (255, 255, 255))
		self.screen.blit(round_num, (10, 10))

	def run_game(self):
		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos() 
					for i in self.nodes:
						if self.nodes[i]['object'].collidepoint(mouse_pos):
							self.node_selected = i
					if self.next_button['object'].collidepoint(mouse_pos):
						self.next_button['is_clicked'] = True
						self.round += 10
				if event.type == pygame.MOUSEBUTTONUP:
					self.next_button['is_clicked'] = False


			self.screen.fill((0, 0, 0))
			self.screen.blit(self.brasil, (300, 0))

			for i in self.nodes:
				if (i == self.node_selected):
					self.nodes[i]['color'] = (0, 255 ,0)
				else:
					self.nodes[i]['color'] = (255, 0, 0)
				pygame.draw.rect(self.screen, self.nodes[i]['color'], self.nodes[i]['object'])
			
			self._draw_info_board()
			self._draw_connections()
			self._draw_next_round_button()
			self._draw_text()
			pygame.display.flip()
			self.clock.tick(60)
