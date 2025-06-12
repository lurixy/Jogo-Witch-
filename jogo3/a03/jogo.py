import pygame
import sys
import os
import random
import math

# Inicialização do pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Halloween Game")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
DARK_ORANGE = (200, 100, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 100)
PURPLE = (128, 0, 128)
BLUE = (0, 100, 255)

# Fonte
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)

class Projectile:
    def __init__(self, x, y, vel_x, vel_y, projectile_type="fireball"):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.projectile_type = projectile_type
        self.size = random.uniform(8, 15)
        self.life = 300  # Tempo de vida do projétil
        self.trail = []  # Rastro do projétil
        
        # Cores baseadas no tipo
        if projectile_type == "fireball":
            self.color = (255, 100, 0)
            self.glow_color = (255, 200, 100)
        elif projectile_type == "lightning":
            self.color = (100, 200, 255)
            self.glow_color = (200, 230, 255)
        else:  # magic
            self.color = (200, 100, 255)
            self.glow_color = (230, 150, 255)
    
    def update(self):
        # Adicionar posição atual ao rastro
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
        
        # Movimento
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Não aplicar gravidade para projéteis horizontais
        # (comentado para que os fogos voem reto)
        # self.vel_y += 0.1
        
        # Diminuir vida
        self.life -= 1
    
    def draw(self, surface):
        if self.life <= 0:
            return
        
        # Desenhar rastro
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = i / len(self.trail)
            trail_size = int(self.size * alpha * 0.5)
            if trail_size > 0:
                trail_color = tuple(int(c * alpha * 0.5) for c in self.color)
                pygame.draw.circle(surface, trail_color, (int(trail_x), int(trail_y)), trail_size)
        
        # Desenhar brilho
        glow_size = int(self.size + 5)
        pygame.draw.circle(surface, self.glow_color, (int(self.x), int(self.y)), glow_size)
        
        # Desenhar projétil principal
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
        
        # Efeito de brilho interno
        inner_size = int(self.size * 0.6)
        inner_color = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.circle(surface, inner_color, (int(self.x), int(self.y)), inner_size)
    
    def is_alive(self):
        return self.life > 0 and self.x < SCREEN_WIDTH + 50 and self.y < SCREEN_HEIGHT + 50

class Wizard:
    def __init__(self, x, y, wizard_type="fire"):
        self.x = x
        self.y = y
        self.initial_y = y  # Posição inicial Y para referência
        self.wizard_type = wizard_type
        self.attack_timer = 0
        self.attack_cooldown = random.randint(60, 120)  # Frames entre ataques
        self.animation_frame = 0
        self.is_attacking = False
        self.attack_duration = 30
        self.current_frame = 0
        self.animation_speed = 10  # Frames entre mudanças de sprite
        self.can_shoot = True  # Controle para atirar apenas quando a tecla for pressionada
        
        # Sistema de movimento vertical
        self.vel_y = 0
        self.jump_speed = -8  # Velocidade de pulo
        self.gravity = 0.4
        self.max_fall_speed = 8
        self.min_y = 100  # Altura máxima que pode alcançar
        self.max_y = SCREEN_HEIGHT - 150  # Altura mínima (chão)
        
        # Carregar sprites baseadas no tipo
        self.sprites = {}
        self.load_sprites(wizard_type)
        
        # Configurações baseadas no tipo
        if wizard_type == "fire":
            self.color = (255, 100, 50)
            self.projectile_type = "fireball"
        elif wizard_type == "lightning":
            self.color = (100, 150, 255)
            self.projectile_type = "lightning"
        else:  # wanderer
            self.color = (150, 100, 255)
            self.projectile_type = "magic"
    
    def load_sprites(self, wizard_type):
        try:
            # Definir caminhos baseados no tipo de mago
            if wizard_type == "fire":
                sprite_folder = os.path.join("..", "craftpix-net-602985-free-wizard-sprite-sheets-pixel-art", "Fire vizard")
                # Para Fire Vizard: spritesheet 896x128, 7 frames de idle (cada frame 128x128)
                idle_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Idle.png"))
                self.sprites['idle'] = self.extract_frames(idle_spritesheet, 7, 128, 128)
                
                # Carregar charge para efeitos de fogo
                charge_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Charge.png"))
                self.sprites['charge'] = self.extract_frames(charge_spritesheet, 7, 128, 128)
                
                # Carregar outras animações
                attack1_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Attack_1.png"))
                self.sprites['attack1'] = self.extract_frames(attack1_spritesheet, 7, 128, 128)
                
                attack2_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Attack_2.png"))
                self.sprites['attack2'] = self.extract_frames(attack2_spritesheet, 7, 128, 128)
                
            elif wizard_type == "lightning":
                sprite_folder = os.path.join("..", "craftpix-net-602985-free-wizard-sprite-sheets-pixel-art", "Lightning Mage")
                # Assumindo mesmo formato para Lightning Mage
                idle_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Idle.png"))
                self.sprites['idle'] = self.extract_frames(idle_spritesheet, 7, 128, 128)
                
                charge_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Charge.png"))
                self.sprites['charge'] = self.extract_frames(charge_spritesheet, 7, 128, 128)
                
                attack1_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Attack_1.png"))
                self.sprites['attack1'] = self.extract_frames(attack1_spritesheet, 7, 128, 128)
                
                attack2_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Attack_2.png"))
                self.sprites['attack2'] = self.extract_frames(attack2_spritesheet, 7, 128, 128)
                
            else:  # wanderer
                sprite_folder = os.path.join("..", "craftpix-net-602985-free-wizard-sprite-sheets-pixel-art", "Wanderer Magican")
                # Assumindo mesmo formato para Wanderer
                idle_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Idle.png"))
                self.sprites['idle'] = self.extract_frames(idle_spritesheet, 7, 128, 128)
                
                charge1_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Charge_1.png"))
                self.sprites['charge'] = self.extract_frames(charge1_spritesheet, 7, 128, 128)
                
                attack1_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Attack_1.png"))
                self.sprites['attack1'] = self.extract_frames(attack1_spritesheet, 7, 128, 128)
                
                attack2_spritesheet = pygame.image.load(os.path.join(sprite_folder, "Attack_2.png"))
                self.sprites['attack2'] = self.extract_frames(attack2_spritesheet, 7, 128, 128)
            
        except pygame.error as e:
            print(f"Erro ao carregar sprites do mago {wizard_type}: {e}")
            # Criar uma sprite padrão se não conseguir carregar
            default_surface = pygame.Surface((64, 64))
            default_surface.fill(self.color)
            self.sprites['idle'] = [default_surface]
            self.sprites['charge'] = [default_surface]
            self.sprites['attack1'] = [default_surface]
            self.sprites['attack2'] = [default_surface]
    
    def extract_frames(self, spritesheet, num_frames, frame_width, frame_height):
        """Extrai frames individuais de um spritesheet"""
        frames = []
        for i in range(num_frames):
            # Calcular posição do frame no spritesheet
            x = i * frame_width
            y = 0
            
            # Criar superfície para o frame
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(spritesheet, (0, 0), (x, y, frame_width, frame_height))
            
            # Redimensionar o frame
            scaled_frame = pygame.transform.scale(frame_surface, (frame_width // 2, frame_height // 2))
            frames.append(scaled_frame)
        
        return frames
    
    def update(self):
        self.animation_frame += 1
        
        # Aplicar gravidade
        self.vel_y += self.gravity
        if self.vel_y > self.max_fall_speed:
            self.vel_y = self.max_fall_speed
        
        # Atualizar posição Y
        self.y += self.vel_y
        
        # Limitar movimento vertical
        if self.y < self.min_y:
            self.y = self.min_y
            self.vel_y = 0
        elif self.y > self.max_y:
            self.y = self.max_y
            self.vel_y = 0
        
        if self.is_attacking:
            self.attack_timer += 1
            if self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.attack_timer = 0
        return False
    
    def jump_up(self):
        """Pular para cima"""
        if self.y > self.min_y:
            self.vel_y = self.jump_speed
    
    def jump_down(self):
        """Pular para baixo (acelerar queda)"""
        if self.y < self.max_y:
            self.vel_y += 3  # Acelera a descida
    
    def shoot(self):
        """Método para atirar quando o jogador pressionar a tecla"""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = 0
            return True  # Sinal para criar projétil
        return False
    
    def draw(self, surface):
        # Determinar qual sprite usar
        if self.is_attacking:
            # Usar animação de charge durante o ataque
            current_sprite_list = self.sprites['charge']
        else:
            current_sprite_list = self.sprites['idle']
        
        # Calcular qual frame da animação mostrar
        frame_index = (self.animation_frame // self.animation_speed) % len(current_sprite_list)
        current_sprite = current_sprite_list[frame_index]
        
        # Desenhar sombra no chão
        ground_y = min(self.y + 40, SCREEN_HEIGHT - 20)  # Garantir que a sombra não saia da tela
        shadow_rect = pygame.Rect(self.x - 25, ground_y - 5, 50, 10)
        pygame.draw.ellipse(surface, (50, 50, 50), shadow_rect)
        
        # Calcular posição para centralizar a sprite
        sprite_rect = current_sprite.get_rect()
        sprite_rect.center = (self.x, self.y)
        
        # Desenhar a sprite do mago
        surface.blit(current_sprite, sprite_rect)
        
        # Efeito de brilho durante ataque
        if self.is_attacking:
            # Criar efeitos de partículas mágicas ao redor do mago
            for i in range(5):
                particle_x = self.x + random.randint(-30, 30)
                particle_y = self.y + random.randint(-30, 30)
                particle_size = random.randint(2, 5)
                pygame.draw.circle(surface, self.color, (particle_x, particle_y), particle_size)
    
    def get_projectile_spawn_point(self):
        return (self.x + 35, self.y - 5)

class Bat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-4, -2)  # Velocidade para a esquerda
        self.vel_y = random.uniform(-1, 1)   # Movimento vertical aleatório
        self.size = random.uniform(15, 25)
        self.wing_flap = 0
        self.flap_speed = random.uniform(0.3, 0.6)
        self.health = 1
        self.color = (50, 20, 50)  # Cor roxa escura
        self.eye_color = (255, 0, 0)  # Olhos vermelhos
        
    def update(self):
        # Movimento
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Leve oscilação vertical
        self.vel_y += random.uniform(-0.1, 0.1)
        self.vel_y = max(-2, min(2, self.vel_y))  # Limitar movimento vertical
        
        # Animação das asas
        self.wing_flap += self.flap_speed
        
    def draw(self, surface):
        # Calcular posição das asas baseado no flap
        wing_offset = math.sin(self.wing_flap) * 8
        
        # Corpo do morcego
        body_size = int(self.size * 0.6)
        pygame.draw.ellipse(surface, self.color, (self.x - body_size//2, self.y - body_size//4, body_size, body_size//2))
        
        # Asas
        wing_size = int(self.size)
        # Asa esquerda
        wing_left = [
            (self.x - wing_size//2, self.y + wing_offset),
            (self.x - wing_size, self.y - wing_size//3 + wing_offset),
            (self.x - wing_size//3, self.y - wing_size//4 + wing_offset)
        ]
        pygame.draw.polygon(surface, self.color, wing_left)
        
        # Asa direita
        wing_right = [
            (self.x + wing_size//2, self.y + wing_offset),
            (self.x + wing_size, self.y - wing_size//3 + wing_offset),
            (self.x + wing_size//3, self.y - wing_size//4 + wing_offset)
        ]
        pygame.draw.polygon(surface, self.color, wing_right)
        
        # Olhos vermelhos
        eye_size = 3
        pygame.draw.circle(surface, self.eye_color, (int(self.x - 5), int(self.y - 3)), eye_size)
        pygame.draw.circle(surface, self.eye_color, (int(self.x + 5), int(self.y - 3)), eye_size)
        
    def is_alive(self):
        return self.health > 0 and self.x > -50
    
    def get_rect(self):
        """Retorna um retângulo para detecção de colisão"""
        size = int(self.size)
        return pygame.Rect(self.x - size//2, self.y - size//2, size, size)

class Ember:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-0.5, 0.5)
        self.vel_y = random.uniform(-2.0, -0.5)
        self.size = random.uniform(2, 6)
        self.life = random.uniform(100, 200)
        self.max_life = self.life
        self.color_intensity = random.uniform(0.7, 1.0)
        self.flicker_speed = random.uniform(0.05, 0.15)
        self.flicker_offset = random.uniform(0, math.pi * 2)
        
    def update(self):
        # Movimento
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Leve movimento horizontal oscilante
        self.vel_x += random.uniform(-0.1, 0.1)
        self.vel_x = max(-1, min(1, self.vel_x))  # Limitar velocidade
        
        # Diminuir vida
        self.life -= 1
        
        # Diminuir tamanho conforme a vida diminui
        life_ratio = self.life / self.max_life
        self.size = max(1, self.size * 0.998)
        
    def draw(self, surface):
        if self.life <= 0:
            return
            
        # Calcular cor baseada na vida e efeito de tremulação
        life_ratio = self.life / self.max_life
        flicker = math.sin(pygame.time.get_ticks() * self.flicker_speed + self.flicker_offset) * 0.3 + 0.7
        
        # Cores que mudam do amarelo para vermelho conforme a brasa "morre"
        if life_ratio > 0.7:
            # Amarelo/laranja brilhante
            r = int(255 * self.color_intensity * flicker)
            g = int(200 * self.color_intensity * flicker)
            b = int(50 * self.color_intensity * flicker)
        elif life_ratio > 0.3:
            # Laranja para vermelho
            r = int(255 * self.color_intensity * flicker)
            g = int((150 * life_ratio) * self.color_intensity * flicker)
            b = int(30 * self.color_intensity * flicker)
        else:
            # Vermelho escurecendo
            r = int((200 * life_ratio) * self.color_intensity * flicker)
            g = int((50 * life_ratio) * self.color_intensity * flicker)
            b = int(10 * self.color_intensity * flicker)
        
        # Garantir que os valores estão no range válido
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        # Desenhar a brasa com um efeito de brilho
        size = int(self.size * life_ratio)
        if size > 0:
            # Brilho externo (mais transparente)
            glow_size = size + 2
            glow_color = (r//3, g//3, b//3)
            pygame.draw.circle(surface, glow_color, (int(self.x), int(self.y)), glow_size)
            
            # Brasa principal
            pygame.draw.circle(surface, (r, g, b), (int(self.x), int(self.y)), size)
    
    def is_alive(self):
        return self.life > 0 and self.y > -50

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    EXIT = "exit"

class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = True  # Controle de tela cheia (começa em tela cheia)
        
        # Sistema de partículas de brasas
        self.embers = []
        self.ember_spawn_timer = 0
        
        # Sistema de animação do background
        self.bg_x = 0  # Posição horizontal do background
        self.bg_speed = 0.5  # Velocidade de movimento (pixels por frame)
        
        # Sistema de jogo
        self.wizards = []
        self.projectiles = []
        self.bats = []  # Lista de morcegos
        self.wizard_spawn_timer = 0
        self.bat_spawn_timer = 0
        self.score = 0  # Pontuação do jogador
        
        # Carregar o background do menu
        try:
            background_path = os.path.join("..", "craftpix-671123-free-halloween-2d-game-backgrounds", 
                                         "PNG", "4_game_background", "4_game_background.png")
            self.menu_bg = pygame.image.load(background_path)
            self.menu_bg = pygame.transform.scale(self.menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Não foi possível carregar o background. Usando cor sólida.")
            self.menu_bg = None
        
        # Carregar background do jogo
        try:
            game_bg_path = os.path.join("..", "craftpix-671123-free-halloween-2d-game-backgrounds", 
                                       "PNG", "1_game_background", "1_game_background.png")
            self.game_bg = pygame.image.load(game_bg_path)
            self.game_bg = pygame.transform.scale(self.game_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Não foi possível carregar o background do jogo. Usando cor sólida.")
            self.game_bg = None
        
        # Botões do menu
        self.menu_buttons = [
            {"text": "NEW GAME", "rect": pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50, 300, 60), "action": "new_game"},
            {"text": "EXIT", "rect": pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 30, 300, 60), "action": "exit"}
        ]
        
        self.selected_button = 0
    
    def toggle_fullscreen(self):
        """Alternar entre tela cheia e janela"""
        global screen
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def handle_menu_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.menu_buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.menu_buttons)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.execute_menu_action()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False  # Permite sair do jogo com ESC no menu
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()  # F11 para alternar tela cheia
            
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, button in enumerate(self.menu_buttons):
                    if button["rect"].collidepoint(mouse_pos):
                        self.selected_button = i
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    mouse_pos = event.pos
                    for button in self.menu_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            self.execute_menu_action()
    
    def execute_menu_action(self):
        action = self.menu_buttons[self.selected_button]["action"]
        if action == "new_game":
            self.state = GameState.PLAYING
            # Inicializar o jogo com apenas um mago Fire Vizard
            self.wizards = []
            self.projectiles = []
            self.bats = []
            self.wizard_spawn_timer = 0
            self.bat_spawn_timer = 0
            self.score = 0
            
            # Criar apenas um mago Fire Vizard no canto esquerdo da tela
            spawn_x = 100  # Posição no canto esquerdo
            spawn_y = SCREEN_HEIGHT - 200  # Bem à frente do cenário
            self.wizards.append(Wizard(spawn_x, spawn_y, "fire"))
            print("Iniciando novo jogo...")
        elif action == "exit":
            self.running = False
    
    def draw_menu(self):
        # Atualizar e gerenciar brasas
        self.update_embers()
        
        # Atualizar posição do background
        self.bg_x -= self.bg_speed
        # Reset da posição quando o background sair completamente da tela
        if self.bg_x <= -SCREEN_WIDTH:
            self.bg_x = 0
        
        # Desenhar background com scroll infinito
        if self.menu_bg:
            # Desenhar a primeira imagem
            screen.blit(self.menu_bg, (self.bg_x, 0))
            # Desenhar a segunda imagem para criar o efeito infinito
            screen.blit(self.menu_bg, (self.bg_x + SCREEN_WIDTH, 0))
        else:
            screen.fill((50, 25, 100))  # Cor de fundo alternativa
        
        # Desenhar brasas atrás do conteúdo do menu
        for ember in self.embers:
            ember.draw(screen)
        
        # Título do jogo
        title_text = font_large.render("HALLOWEEN GAME", True, ORANGE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        
        # Sombra do título
        title_shadow = font_large.render("HALLOWEEN GAME", True, BLACK)
        shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 3, SCREEN_HEIGHT//4 + 3))
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title_text, title_rect)
        
        # Desenhar botões
        for i, button in enumerate(self.menu_buttons):
            # Cor do botão (destacado se selecionado)
            if i == self.selected_button:
                button_color = ORANGE
                text_color = BLACK
                border_color = WHITE
            else:
                button_color = DARK_ORANGE
                text_color = WHITE
                border_color = ORANGE
            
            # Desenhar retângulo do botão
            pygame.draw.rect(screen, button_color, button["rect"])
            pygame.draw.rect(screen, border_color, button["rect"], 3)
            
            # Desenhar texto do botão
            button_text = font_medium.render(button["text"], True, text_color)
            text_rect = button_text.get_rect(center=button["rect"].center)
            screen.blit(button_text, text_rect)
        
        # Instruções
        instruction_text = font_small.render("Use as setas ou mouse para navegar", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 80))
        screen.blit(instruction_text, instruction_rect)
        
        enter_text = font_small.render("ENTER/ESPAÇO para selecionar", True, WHITE)
        enter_rect = enter_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        screen.blit(enter_text, enter_rect)
    
    def update_embers(self):
        # Atualizar brasas existentes
        for ember in self.embers[:]:  # Cópia da lista para iterar
            ember.update()
            if not ember.is_alive():
                self.embers.remove(ember)
        
        # Gerar novas brasas
        self.ember_spawn_timer += 1
        if self.ember_spawn_timer >= 8:  # Gerar nova brasa a cada 8 frames
            # Gerar brasas principalmente na parte inferior da tela, mas dentro dos limites
            spawn_x = random.randint(50, SCREEN_WIDTH - 50)
            spawn_y = random.randint(SCREEN_HEIGHT - 80, SCREEN_HEIGHT - 20)
            self.embers.append(Ember(spawn_x, spawn_y))
            self.ember_spawn_timer = 0
        
        # Limitar número de brasas para performance
        if len(self.embers) > 50:
            self.embers = self.embers[-40:]  # Manter apenas as 40 mais recentes
    
    def handle_game_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                elif event.key == pygame.K_RIGHT:
                    # Atirar projétil quando pressionar seta direita
                    for wizard in self.wizards:
                        should_shoot = wizard.shoot()
                        if should_shoot:
                            # Criar projétil
                            spawn_x, spawn_y = wizard.get_projectile_spawn_point()
                            # Atirar para a direita (horizontal)
                            vel_x = 8  # Velocidade para a direita
                            vel_y = 0  # Sem movimento vertical
                            projectile = Projectile(spawn_x, spawn_y, vel_x, vel_y, wizard.projectile_type)
                            self.projectiles.append(projectile)
                elif event.key == pygame.K_UP:
                    # Pular para cima
                    for wizard in self.wizards:
                        wizard.jump_up()
                elif event.key == pygame.K_DOWN:
                    # Pular para baixo
                    for wizard in self.wizards:
                        wizard.jump_down()
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()  # F11 para alternar tela cheia
    
    def update_game(self):
        # Atualizar magos existentes
        for wizard in self.wizards[:]:
            wizard.update()  # Não mais atirar automaticamente
        
        # Atualizar projéteis
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.is_alive():
                self.projectiles.remove(projectile)
        
        # Atualizar morcegos
        for bat in self.bats[:]:
            bat.update()
            if not bat.is_alive():
                self.bats.remove(bat)
        
        # Verificar colisões entre projéteis e morcegos
        for projectile in self.projectiles[:]:
            projectile_rect = pygame.Rect(projectile.x - projectile.size, projectile.y - projectile.size, 
                                        projectile.size * 2, projectile.size * 2)
            for bat in self.bats[:]:
                bat_rect = bat.get_rect()
                if projectile_rect.colliderect(bat_rect):
                    # Colisão detectada!
                    self.bats.remove(bat)
                    self.projectiles.remove(projectile)
                    self.score += 10  # Aumentar pontuação
                    break
        
        # Spawnar novos morcegos
        self.bat_spawn_timer += 1
        if self.bat_spawn_timer >= 120:  # Novo morcego a cada 2 segundos
            # Spawnar morcegos do lado direito da tela
            spawn_x = SCREEN_WIDTH + 50
            spawn_y = random.randint(100, SCREEN_HEIGHT - 100)
            self.bats.append(Bat(spawn_x, spawn_y))
            self.bat_spawn_timer = 0
        
        # Limitar número de morcegos para performance
        if len(self.bats) > 10:
            self.bats = self.bats[-8:]  # Manter apenas os 8 mais recentes
        
        # Não spawnar novos magos - manter apenas o único mago
        # Comentando o código de spawn para manter apenas um mago
        # self.wizard_spawn_timer += 1
        # if self.wizard_spawn_timer >= 180:  # Novo mago a cada 3 segundos (60 FPS * 3)
        #     wizard_types = ["fire", "lightning", "wanderer"]
        #     wizard_type = random.choice(wizard_types)
        #     # Spawnar magos em posições aleatórias na parte inferior
        #     spawn_x = random.randint(50, SCREEN_WIDTH - 50)
        #     spawn_y = random.randint(SCREEN_HEIGHT - 150, SCREEN_HEIGHT - 100)
        #     self.wizards.append(Wizard(spawn_x, spawn_y, wizard_type))
        #     self.wizard_spawn_timer = 0
        
        # Não limitar número de magos já que temos apenas um
        # if len(self.wizards) > 8:
        #     self.wizards = self.wizards[-6:]  # Manter apenas os 6 mais recentes
    
    def draw_game(self):
        # Desenhar background do jogo
        if self.game_bg:
            screen.blit(self.game_bg, (0, 0))
        else:
            screen.fill((30, 15, 60))  # Fundo roxo escuro
        
        # Atualizar lógica do jogo
        self.update_game()
        
        # Desenhar magos
        for wizard in self.wizards:
            wizard.draw(screen)
        
        # Desenhar projéteis
        for projectile in self.projectiles:
            projectile.draw(screen)
        
        # Desenhar morcegos
        for bat in self.bats:
            bat.draw(screen)
        
        # UI do jogo
        # Pontuação
        score_text = font_small.render(f"Pontuação: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Contador de magos
        wizard_text = font_small.render(f"Magos: {len(self.wizards)}", True, WHITE)
        screen.blit(wizard_text, (10, 40))
        
        # Contador de projéteis
        projectile_text = font_small.render(f"Projéteis: {len(self.projectiles)}", True, WHITE)
        screen.blit(projectile_text, (10, 70))
        
        # Contador de morcegos
        bat_text = font_small.render(f"Morcegos: {len(self.bats)}", True, WHITE)
        screen.blit(bat_text, (10, 100))
        
        # Instrução para voltar ao menu
        back_text = font_small.render("ESC: Menu", True, WHITE)
        back_rect = back_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(back_text, back_rect)
        
        # Instrução para atirar
        shoot_text = font_small.render("SETA DIREITA: Atirar", True, WHITE)
        shoot_rect = shoot_text.get_rect(topright=(SCREEN_WIDTH - 10, 35))
        screen.blit(shoot_text, shoot_rect)
        
        # Instruções de movimento
        move_text = font_small.render("SETAS CIMA/BAIXO: Pular", True, WHITE)
        move_rect = move_text.get_rect(topright=(SCREEN_WIDTH - 10, 60))
        screen.blit(move_text, move_rect)
    
    def run(self):
        while self.running:
            events = pygame.event.get()
            
            # Verificar se o usuário fechou a janela
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Limpar a tela completamente
            screen.fill(BLACK)
            
            # Processar eventos baseado no estado atual
            if self.state == GameState.MENU:
                self.handle_menu_events(events)
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.handle_game_events(events)
                self.draw_game()
            
            # Forçar atualização da tela
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()