import pygame
import os
import time
import random
pygame.font.init()

# Colors
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
ICON = pygame.transform.rotate(pygame.image.load(os.path.join('ressources', 'spaceship_red.png')), 180)
pygame.display.set_icon(ICON)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 50

# Load images

# Player ship
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("ressources", "spaceship_red.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# Enemies ship
YELLOW_SPACESHIP =  pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("ressources", "spaceship_yellow.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
PURPLE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("ressources", "spaceship_purple.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
CYAN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("ressources", "spaceship_cyan.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("ressources", "spaceship_green.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Lasers
RED_LASER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("ressources", "pixel_laser_red.png")), (50, 55)), 90)
YELLOW_LASER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("ressources", "pixel_laser_yellow.png")), (50, 55)), 90)
PURPLE_LASER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("ressources", "pixel_laser_purple.png")), (50, 55)), 90)
CYAN_LASER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("ressources", "pixel_laser_cyan.png")), (50, 55)), 90)
GREEN_LASER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("ressources", "pixel_laser_green.png")), (50, 55)), 90)

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("ressources", "space.png")), (WIDTH, HEIGHT))

class Laser:
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self, window):
		window.blit(self.img, (self.x, self.y))

	def move(self, vel):
		self.x -= vel

	def off_screen(self, width):
		return self.x <= 0 and self.x >= width

	def collision(self, obj):
		return collide(obj, self)



class Ship:
	COOLDOWN = 30

	def __init__(self, x, y, color, health = 100):
		self.x = x
		self.y = y
		self.health = health
		self.ship_img = None
		self.laser_img = None
		self.lasers = []
		self.cool_down_counter = 0

	def draw(self, window):
		window.blit(self.ship_img, (self.x, self.y))
		for laser in self.lasers:
			laser.draw(window)

	def move_lasers(self, vel, obj):
		self.cooldown()
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(WIDTH): #############################################################################################################################
				self.laser.remove(laser)
			elif laser.collision(obj):
				obj.health -= 10
				self.lasers.remove(laser)

	def cooldown(self):
		if self.cool_down_counter >= self.COOLDOWN:
			self.cool_down_counter = 0
		elif self.cool_down_counter > 0:
			self.cool_down_counter += 1

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x, self.y, self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter = 1

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()

class Player(Ship):
	def __init__(self, x, y, health = 100):
		super().__init__(x, y, health)
		self.ship_img = RED_SPACESHIP
		self.laser_img = RED_LASER
		self.mask = pygame.mask.from_surface(self.ship_img) # this line defines the true hitbox with the pixels
		self.max_health = health

	def move_lasers(self, vel, objs):
		self.cooldown()
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(0): #############################################################################################################################
				self.laser.remove(laser)
			else:
				for obj in objs:
					if laser.collision(obj):
						objs.remove(obj)
						if laser in self.lasers:
							self.lasers.remove(laser)

	def draw(self, window):
		super().draw(window)
		self.healthbar(window)

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x + 25, self.y + 3, self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter = 1

	def healthbar(self, window):
		pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 5))
		pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 5))

class Enemy(Ship):
	COLOR_MAP = {
				"yellow": (YELLOW_SPACESHIP, YELLOW_LASER),
				"purple": (PURPLE_SPACESHIP, PURPLE_LASER),
				"cyan": (CYAN_SPACESHIP, CYAN_LASER),
				"green": (GREEN_SPACESHIP, GREEN_LASER) 
	}
	def __init__(self, x, y, color, health = 100):
		super().__init__(x, y, health)
		self.ship_img, self.laser_img = self.COLOR_MAP[color]
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.color = color

	def move(self, vel):
		
		#if self.color == "green":
			#self.x -= 5 * vel
		#else:
			self.x -= vel

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x - 30, self.y + 3, self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter = 1

def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
	run = True
	FPS = 60
	level = 0
	lives = 5
	main_font = pygame.font.SysFont("comicsans", 40)
	lost_font = pygame.font.SysFont("comicsans", 60)

	enemies = []
	wave_length = 5
	enemy_vel = 1 

	player_vel = 5
	laser_vel =  5

	player = Player(0, HEIGHT//2 - 50)

	clock = pygame.time.Clock()

	lost = False
	lost_count = 0

	def redraw_window():
		WIN.blit(BG, (0, 0))
		# Draw Text
		lives_label = main_font.render(f"Lives: {lives}", 1, WHITE)
		level_label = main_font.render(f"Level: {level}", 1, WHITE)

		WIN.blit(lives_label, (10, 10))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
		
		for enemy in enemies:
			enemy.draw(WIN)

		player.draw(WIN)

		if lost:
			lost_label = lost_font.render("You Lost!", 1, WHITE)
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 200))


		pygame.display.update()

	while run:
		clock.tick(FPS) # this must be at the top of the while loop
		redraw_window()

		if lives <= 0 or player.health <= 0:
			lost = True
			lost_count += 1

		if lost:
			if lost_count > FPS * 3:
				run = False
			else:
				continue
		
		if len(enemies) == 0:
			level += 1
			wave_length += 5
			for i in range(wave_length):
				enemy = Enemy(random.randrange(WIDTH + 100, WIDTH + 1500), random.randrange(50, HEIGHT - 100), random.choice(["yellow", "purple", "cyan", "green"]))
				enemies.append(enemy)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		keys = pygame.key.get_pressed()
		if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y > 0:
			player.y -= player_vel
		if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y < HEIGHT - player.get_height():
			player.y += player_vel
		if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > 0:
			player.x -= player_vel
		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x < WIDTH - player.get_width():
			player.x += player_vel
		if keys[pygame.K_SPACE]:
			player.shoot()

		for enemy in enemies[:]:
			enemy.move(enemy_vel)
			enemy.move_lasers(laser_vel, player)

			if random.randrange(0, 3* FPS) == 1:
				enemy.shoot()

			if collide(enemy, player):
				lives -= 1
				enemies.remove(enemy)
			elif enemy.x < 0:
				lives -= 1
				enemies.remove(enemy)	


		player.move_lasers(- laser_vel, enemies)

def main_menu():
	title_font = pygame.font.SysFont("comicsans", 70)
	instructions_font = pygame.font.SysFont("comicsans", 40)
	run = True
	while run:
		WIN.blit(BG, (0, 0))
		title_label = title_font.render("Press the mouse button to begin...", 1, (WHITE))
		instructions_label = instructions_font.render("WASD/Arrows to move and SpaceBar to shoot", 1, (WHITE))
		WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 200))
		WIN.blit(instructions_label, (WIDTH/2 - instructions_label.get_width()/2, 300))
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				main()

	pygame.quit()

if __name__ == "__main__":		
	main_menu()