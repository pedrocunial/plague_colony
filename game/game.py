import pygame

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((1920, 1080))
		self.done = False
		self.clock = pygame.time.Clock()
		self.size_square = 20
	
	def create_objects(self):
		self.brasil = pygame.image.load('Pictures/mapa_brasil.png')
		self.nodes = {}
		self._create_tribes()

	def _create_node(self, x, y, color):
			return {'object': pygame.Rect(x, y, self.size_square, self.size_square), 'color': color}

	def _create_tribes(self):
		self.nodes['tupi_2'] = self._create_node(1200, 300, [255, 0, 0])
		self.nodes['tupi_1'] = self._create_node(700, 300, [255, 0, 0])
		self.nodes['tupi_3'] = self._create_node(800, 600, [255, 0, 0])
		self.nodes['tupi_4'] = self._create_node(700, 300, [255, 0, 0])
		self.nodes['je'] = self._create_node(950, 400, [255, 0, 0])
		self.nodes['je_2'] = self._create_node(900, 700, [255, 0, 0])
		self.nodes['karib'] = self._create_node(700, 150, [255, 0, 0])
		self.nodes['pano'] = self._create_node(400, 300, [255, 0, 0])
		self.nodes['charrua'] = self._create_node(800, 900, [255, 0, 0])
		self.nodes['aruak'] = self._create_node(500, 250, [255, 0, 0])
		self.nodes['tukano'] = self._create_node(550, 175, [255, 0, 0])

	def run_game(self):
		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos() 
					for i in self.nodes:
						if self.nodes[i]['object'].collidepoint(mouse_pos):
							self.nodes[i]['color'] = [0,255,255]
			self.screen.fill((0, 0, 0))
			self.screen.blit(self.brasil, (300, 0))

			for i in self.nodes:
				pygame.draw.rect(self.screen, self.nodes[i]['color'], self.nodes[i]['object'])

			pygame.display.flip()
			self.clock.tick(60)
