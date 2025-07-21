import sys
if sys.version_info >= (3, 7):
    import io
    sys.stdin, sys.stdout, sys.stderr = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8'), io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'), io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pygame
import sys
import os
import random
import math

# Garante que todos os caminhos relativos partam do diretório deste script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

# Inicialização do pygame
pygame.init()

# Configurações da tela
# Detectar resolução da tela automaticamente
pygame.display.init()
info = pygame.display.Info()
NATIVE_WIDTH = info.current_w
NATIVE_HEIGHT = info.current_h

# Definir resolução do jogo mantendo proporção 16:9
# Usar a altura da tela e calcular largura proporcional
SCREEN_HEIGHT = NATIVE_HEIGHT
SCREEN_WIDTH = int(SCREEN_HEIGHT * 16 / 9)

# Se a largura calculada for maior que a tela, usar a largura da tela
if SCREEN_WIDTH > NATIVE_WIDTH:
    SCREEN_WIDTH = NATIVE_WIDTH
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 9 / 16)

print(f"Resolução detectada: {NATIVE_WIDTH}x{NATIVE_HEIGHT}")
print(f"Resolução do jogo: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

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

# Fontes
try:
    # Lista de fontes góticas/macabras para tentar (em ordem de preferência)
    gothic_fonts = [
        'ghoulish fright aoe',  # Fonte sugerida no readme
        'creepster',           # Fonte estilo gotejante do Google Fonts
        'nosifer',             # Fonte sangrenta do Google Fonts
        'butcherman',          # Fonte macabra do Google Fonts
        'eater',               # Fonte corrosiva do Google Fonts
        'frightened',          # Fonte de terror
        'blood crow',          # Fonte estilo sangue
        'horror house',        # Fonte de casa assombrada
        'zombie holocaust',    # Fonte zombie
        'chiller',             # Fonte padrão mais comum
        'ravie',               # Fonte decorativa alternativa
        'jokerman',            # Fonte divertida/macabra
        'showcard gothic'      # Fonte gótica alternativa
    ]
    
    # Tentar carregar fontes góticas em ordem de preferência
    font_large = None
    font_medium = None
    
    for font_name in gothic_fonts:
        try:
            test_font = pygame.font.SysFont(font_name, 90)
            if test_font:
                font_large = pygame.font.SysFont(font_name, 90)
                font_medium = pygame.font.SysFont(font_name, 60)
                print(f"Fonte gótica carregada: {font_name}")
                break
        except:
            continue
    
    # Se não encontrou nenhuma fonte gótica, usar fallback
    if not font_large:
        font_large = pygame.font.SysFont('chiller', 90)
        font_medium = pygame.font.SysFont('chiller', 60)
        print("Usando fonte fallback: chiller")
    
    # Fontes menores permanecem simples para legibilidade
    font_small = pygame.font.SysFont('arial', 24)
    font_tiny = pygame.font.SysFont('arial', 18)
    
    # Fontes especiais para título - versões maiores e mais dramáticas
    font_title = None
    font_title_mega = None
    
    # Tentar criar fontes de título maiores
    if font_large:
        # Fonte atual encontrada
        current_font_name = font_name if 'font_name' in locals() else 'chiller'
        font_title = pygame.font.SysFont(current_font_name, 150)  # Muito maior para título
        font_title_mega = pygame.font.SysFont(current_font_name, 180)  # Ainda maior para "HALLOWEEN"
    else:
        font_title = pygame.font.SysFont('chiller', 150)
        font_title_mega = pygame.font.SysFont('chiller', 180)
    
    print(f"Fontes de título criadas: {font_title is not None}")
    
except:
    # Fallback final para fontes padrão se não encontrar nenhuma
    font_large = pygame.font.Font(None, 90)
    font_medium = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 18)
    font_title = pygame.font.Font(None, 150)
    font_title_mega = pygame.font.Font(None, 180)
    print("Usando fontes padrão do sistema")

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
        elif projectile_type == "magic_arrow":
            self.color = (139, 69, 19)  # Cor marrom para flecha
            self.glow_color = (205, 133, 63)
        elif projectile_type == "sword_slash":
            self.color = (255, 215, 0)  # Cor dourada para espada
            self.glow_color = (255, 255, 150)
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
        
        # Desenhar projétil específico baseado no tipo
        if self.projectile_type == "magic_arrow":
            # Desenhar flecha
            arrow_length = int(self.size * 2)
            arrow_width = int(self.size * 0.8)
            
            # Corpo da flecha
            pygame.draw.line(surface, self.color, 
                           (int(self.x - arrow_length), int(self.y)), 
                           (int(self.x + arrow_length), int(self.y)), 3)
            
            # Ponta da flecha
            arrow_head = [
                (int(self.x + arrow_length), int(self.y)),
                (int(self.x + arrow_length - arrow_width), int(self.y - arrow_width//2)),
                (int(self.x + arrow_length - arrow_width), int(self.y + arrow_width//2))
            ]
            pygame.draw.polygon(surface, self.color, arrow_head)
            
            # Empenas da flecha
            pygame.draw.line(surface, self.color, 
                           (int(self.x - arrow_length), int(self.y - 3)), 
                           (int(self.x - arrow_length + 5), int(self.y)), 2)
            pygame.draw.line(surface, self.color, 
                           (int(self.x - arrow_length), int(self.y + 3)), 
                           (int(self.x - arrow_length + 5), int(self.y)), 2)
        elif self.projectile_type == "sword_slash":
            # Desenhar corte de espada (linha dourada com efeito)
            slash_length = int(self.size * 3)
            slash_width = int(self.size * 0.6)
            
            # Múltiplas linhas para efeito de corte
            for i in range(5):
                alpha = (5 - i) / 5
                line_color = tuple(int(c * alpha) for c in self.color)
                offset = i * 2
                
                pygame.draw.line(surface, line_color, 
                               (int(self.x - slash_length + offset), int(self.y - slash_width + offset)), 
                               (int(self.x + slash_length + offset), int(self.y + slash_width + offset)), 4)
                
            # Brilho principal do corte
            pygame.draw.line(surface, self.glow_color, 
                           (int(self.x - slash_length), int(self.y - slash_width)), 
                           (int(self.x + slash_length), int(self.y + slash_width)), 6)
        else:
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
        
        # Carregar sprites baseadas no tipo de mago
        self.sprites = {}
        self.load_sprites(wizard_type)
        
        # Configurações baseadas no tipo
        if wizard_type == "fire":
            self.color = (255, 100, 50)
            self.projectile_type = "fireball"
        elif wizard_type == "lightning":
            self.color = (100, 150, 255)
            self.projectile_type = "lightning"
        elif wizard_type == "sword":
            self.color = (200, 200, 50)  # Cor dourada para espada
            self.projectile_type = "sword_slash"
        else:  # wanderer
            self.color = (150, 100, 255)
            self.projectile_type = "magic_arrow"
    
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
            
            # Redimensionar o frame para um tamanho maior (120% do original para máxima visibilidade)
            new_width = int(frame_width * 1.2)
            new_height = int(frame_height * 1.2)
            scaled_frame = pygame.transform.scale(frame_surface, (new_width, new_height))
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
        
        # Adicionar leve pulsação durante idle para maior presença visual
        if not self.is_attacking:
            # Pulsação sutil entre 100% e 105% do tamanho base
            pulse_factor = 1.0 + 0.05 * math.sin(self.animation_frame * 0.1)
            pulse_width = int(current_sprite.get_width() * pulse_factor)
            pulse_height = int(current_sprite.get_height() * pulse_factor)
            current_sprite = pygame.transform.scale(current_sprite, (pulse_width, pulse_height))
        
        # Aumentar ainda mais o tamanho durante ataques
        if self.is_attacking:
            # Durante ataques, escalar para 140% do tamanho atual (presença dominante)
            attack_width = int(current_sprite.get_width() * 1.4)
            attack_height = int(current_sprite.get_height() * 1.4)
            current_sprite = pygame.transform.scale(current_sprite, (attack_width, attack_height))
        
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
            # Criar efeitos de partículas mágicas ao redor do mago (mais intensos)
            for i in range(8):  # Mais partículas durante ataque
                particle_x = self.x + random.randint(-40, 40)
                particle_y = self.y + random.randint(-40, 40)
                particle_size = random.randint(3, 8)  # Partículas maiores
                pygame.draw.circle(surface, self.color, (particle_x, particle_y), particle_size)
            
            # Adicionar aura brilhante ao redor do mago durante ataque
            aura_radius = 60
            aura_color = tuple(min(255, c + 100) for c in self.color)
            pygame.draw.circle(surface, (*aura_color, 50), (int(self.x), int(self.y)), aura_radius, 3)
    
    def get_projectile_spawn_point(self):
        return (self.x + 45, self.y - 5)  # Adjusted for larger wizard size

class Bat:
    def __init__(self, x, y, target_wizard=None):
        self.x = x
        self.y = y
        self.target_wizard = target_wizard
        self.vel_x = random.uniform(-4, -2)  # Velocidade base para a esquerda
        self.vel_y = random.uniform(-1, 1)   # Movimento vertical inicial
        self.size = random.uniform(25, 35)  # Tamanho maior para melhor aparência
        self.wing_flap = 0
        self.flap_speed = random.uniform(0.3, 0.6)
        self.health = 1
        self.color = (50, 20, 50)  # Cor roxa escura
        self.wing_color = (40, 15, 40)  # Cor das asas
        self.eye_color = (255, 0, 0)  # Olhos vermelhos
        self.tracking_speed = 1.2  # Velocidade de rastreamento do mago
        
    def update(self):
        # Se tiver um mago alvo, mover em direção a ele
        if self.target_wizard:
            # Calcular direção para o mago
            dx = self.target_wizard.x - self.x
            dy = self.target_wizard.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Normalizar direção e aplicar velocidade de rastreamento
                self.vel_x = (dx / distance) * self.tracking_speed
                self.vel_y = (dy / distance) * self.tracking_speed
        
        # Movimento
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Adicionar oscilação para movimento mais natural
        self.vel_y += random.uniform(-0.08, 0.08)
        
        # Animação das asas
        self.wing_flap += self.flap_speed
        
    def draw(self, surface):
        # Calcular posição das asas baseado no flap
        wing_offset = math.sin(self.wing_flap) * 10
        
        # Corpo do morcego (mais detalhado)
        body_size = int(self.size * 0.7)
        body_rect = pygame.Rect(self.x - body_size//2, self.y - body_size//3, body_size, body_size//1.5)
        pygame.draw.ellipse(surface, self.color, body_rect)
        
        # Contorno do corpo
        pygame.draw.ellipse(surface, (30, 10, 30), body_rect, 2)
        
        # Cabeça maior
        head_size = int(self.size * 0.5)
        head_rect = pygame.Rect(self.x - head_size//2, self.y - body_size//2 - head_size//2, head_size, head_size)
        pygame.draw.ellipse(surface, self.color, head_rect)
        pygame.draw.ellipse(surface, (30, 10, 30), head_rect, 2)
        
        # Asas maiores e mais detalhadas
        wing_size = int(self.size * 1.2)
        # Asa esquerda
        wing_left = [
            (self.x - wing_size//3, self.y + wing_offset),
            (self.x - wing_size, self.y - wing_size//4 + wing_offset),
            (self.x - wing_size*0.8, self.y + wing_size//6 + wing_offset),
            (self.x - wing_size//2, self.y + wing_size//8 + wing_offset)
        ]
        pygame.draw.polygon(surface, self.wing_color, wing_left)
        pygame.draw.polygon(surface, (20, 5, 20), wing_left, 2)
        
        # Asa direita
        wing_right = [
            (self.x + wing_size//3, self.y + wing_offset),
            (self.x + wing_size, self.y - wing_size//4 + wing_offset),
            (self.x + wing_size*0.8, self.y + wing_size//6 + wing_offset),
            (self.x + wing_size//2, self.y + wing_size//8 + wing_offset)
        ]
        pygame.draw.polygon(surface, self.wing_color, wing_right)
        pygame.draw.polygon(surface, (20, 5, 20), wing_right, 2)
        
        # Olhos vermelhos brilhantes maiores
        eye_size = 4
        pygame.draw.circle(surface, self.eye_color, (int(self.x - 8), int(self.y - body_size//4)), eye_size)
        pygame.draw.circle(surface, self.eye_color, (int(self.x + 8), int(self.y - body_size//4)), eye_size)
        
        # Brilho nos olhos
        pygame.draw.circle(surface, (255, 100, 100), (int(self.x - 8), int(self.y - body_size//4)), 2)
        pygame.draw.circle(surface, (255, 100, 100), (int(self.x + 8), int(self.y - body_size//4)), 2)
        
        # Orelhas pontudas
        ear_size = int(self.size * 0.3)
        # Orelha esquerda
        ear_left = [
            (int(self.x - head_size//3), int(self.y - body_size//2 - head_size//2)),
            (int(self.x - head_size//2), int(self.y - body_size//2 - head_size//2 - ear_size)),
            (int(self.x - head_size//4), int(self.y - body_size//2 - head_size//3))
        ]
        pygame.draw.polygon(surface, self.color, ear_left)
        
        # Orelha direita
        ear_right = [
            (int(self.x + head_size//3), int(self.y - body_size//2 - head_size//2)),
            (int(self.x + head_size//2), int(self.y - body_size//2 - head_size//2 - ear_size)),
            (int(self.x + head_size//4), int(self.y - body_size//2 - head_size//3))
        ]
        pygame.draw.polygon(surface, self.color, ear_right)
        
    def is_alive(self):
        return self.health > 0 and self.x > -50
    
    def get_rect(self):
        """Retorna um retângulo para detecção de colisão"""
        size = int(self.size)
        return pygame.Rect(self.x - size//2, self.y - size//2, size, size)

class FlyingWitch:
    def __init__(self, x, y, target_wizard=None):
        self.x = x
        self.y = y
        self.target_wizard = target_wizard
        self.vel_x = random.uniform(-2.5, -1.0)  # Velocidade base para a esquerda
        self.vel_y = random.uniform(-0.5, 0.5)   # Movimento vertical inicial
        self.size = random.uniform(25, 35)  # Tamanho maior para melhor aparência
        self.wing_flap = 0
        self.flap_speed = random.uniform(0.3, 0.6)
        self.health = 1
        self.color = (80, 20, 80)  # Cor roxa escura para bruxa
        self.hat_color = (20, 20, 20)  # Chapéu preto
        self.eye_color = (255, 100, 0)  # Olhos laranja brilhantes
        self.tracking_speed = 0.8  # Velocidade de rastreamento do mago
        
    def update(self):
        # Se tiver um mago alvo, mover em direção a ele
        if self.target_wizard:
            # Calcular direção para o mago
            dx = self.target_wizard.x - self.x
            dy = self.target_wizard.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Normalizar direção e aplicar velocidade de rastreamento
                self.vel_x = (dx / distance) * self.tracking_speed
                self.vel_y = (dy / distance) * self.tracking_speed
        
        # Movimento
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Adicionar um pouco de oscilação para parecer mais natural
        self.vel_y += random.uniform(-0.03, 0.03)
        
        # Animação das asas
        self.wing_flap += self.flap_speed
        
    def draw(self, surface):
        # Calcular posição das asas baseado no flap
        wing_offset = math.sin(self.wing_flap) * 8
        
        # Corpo da bruxa (formato oval maior)
        body_size = int(self.size * 0.8)
        body_rect = pygame.Rect(self.x - body_size//2, self.y - body_size//3, body_size, body_size//1.2)
        pygame.draw.ellipse(surface, self.color, body_rect)
        
        # Contorno do corpo
        pygame.draw.ellipse(surface, (50, 10, 50), body_rect, 2)
        
        # Cabeça maior
        head_size = int(self.size * 0.6)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y - body_size//3)), head_size)
        pygame.draw.circle(surface, (50, 10, 50), (int(self.x), int(self.y - body_size//3)), head_size, 2)
        
        # Chapéu de bruxa (triângulo maior)
        hat_height = int(self.size * 0.8)
        hat_base = int(self.size * 0.6)
        hat_points = [
            (int(self.x), int(self.y - body_size//3 - hat_height)),  # Ponta do chapéu
            (int(self.x - hat_base//2), int(self.y - body_size//3)),  # Base esquerda
            (int(self.x + hat_base//2), int(self.y - body_size//3))   # Base direita
        ]
        pygame.draw.polygon(surface, self.hat_color, hat_points)
        pygame.draw.polygon(surface, (0, 0, 0), hat_points, 2)
        
        # Aba do chapéu
        aba_rect = pygame.Rect(self.x - hat_base//1.2, self.y - body_size//3 - 5, 
                              hat_base*1.6, hat_base//2.5)
        pygame.draw.ellipse(surface, self.hat_color, aba_rect)
        pygame.draw.ellipse(surface, (0, 0, 0), aba_rect, 2)
        
        # Asas maiores e mais detalhadas (formato mais angular para bruxa)
        wing_size = int(self.size * 1.0)
        # Asa esquerda
        wing_left = [
            (self.x - wing_size//4, self.y + wing_offset),
            (self.x - wing_size, self.y - wing_size//4 + wing_offset),
            (self.x - wing_size*0.8, self.y + wing_size//6 + wing_offset),
            (self.x - wing_size//2, self.y + wing_size//8 + wing_offset)
        ]
        pygame.draw.polygon(surface, (40, 10, 40), wing_left)
        pygame.draw.polygon(surface, (20, 5, 20), wing_left, 2)
        
        # Asa direita
        wing_right = [
            (self.x + wing_size//4, self.y + wing_offset),
            (self.x + wing_size, self.y - wing_size//4 + wing_offset),
            (self.x + wing_size*0.8, self.y + wing_size//6 + wing_offset),
            (self.x + wing_size//2, self.y + wing_size//8 + wing_offset)
        ]
        pygame.draw.polygon(surface, (40, 10, 40), wing_right)
        pygame.draw.polygon(surface, (20, 5, 20), wing_right, 2)
        
        # Olhos brilhantes maiores
        eye_size = 4
        pygame.draw.circle(surface, self.eye_color, (int(self.x - 8), int(self.y - body_size//3)), eye_size)
        pygame.draw.circle(surface, self.eye_color, (int(self.x + 8), int(self.y - body_size//3)), eye_size)
        
        # Brilho dos olhos
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x - 8), int(self.y - body_size//3)), 2)
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x + 8), int(self.y - body_size//3)), 2)
        
        # Nariz pontudo da bruxa
        nose_points = [
            (int(self.x), int(self.y - body_size//3 + head_size//4)),
            (int(self.x - 3), int(self.y - body_size//3 + head_size//3)),
            (int(self.x + 3), int(self.y - body_size//3 + head_size//3))
        ]
        pygame.draw.polygon(surface, (60, 15, 60), nose_points)
        
        # Cabelo saindo do chapéu
        hair_points = [
            (int(self.x - hat_base//3), int(self.y - body_size//3)),
            (int(self.x - hat_base//2), int(self.y - body_size//3 + head_size//3)),
            (int(self.x - hat_base//4), int(self.y - body_size//3 + head_size//4))
        ]
        pygame.draw.polygon(surface, (60, 30, 60), hair_points)
        
    def is_alive(self):
        return self.health > 0 and self.x > -50
    
    def get_rect(self):
        """Retorna um retângulo para detecção de colisão"""
        size = int(self.size)
        return pygame.Rect(self.x - size//2, self.y - size//2, size, size)

class Spider:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_y = y  # Posição inicial para a teia
        self.vel_y = random.uniform(1.5, 3.0)  # Velocidade de descida mais rápida
        self.size = random.uniform(20, 30)  # Tamanho da aranha
        self.health = 1
        self.color = (30, 10, 10)  # Cor marrom escura
        self.leg_color = (20, 5, 5)  # Cor das pernas
        self.eye_color = (255, 50, 50)  # Olhos vermelhos
        self.web_color = (200, 200, 200)  # Cor da teia (cinza claro)
        self.swing_amplitude = random.uniform(15, 25)  # Amplitude do balanço
        self.swing_speed = random.uniform(0.05, 0.1)  # Velocidade do balanço
        self.swing_offset = random.uniform(0, math.pi * 2)  # Offset para variação
        self.animation_frame = 0
        
    def update(self):
        # Movimento de descida
        self.y += self.vel_y
        
        # Movimento de balanço da aranha na teia
        swing_x = math.sin(pygame.time.get_ticks() * self.swing_speed + self.swing_offset) * self.swing_amplitude
        self.x = self.x + swing_x * 0.02  # Movimento sutil de balanço
        
        # Animação das pernas
        self.animation_frame += 0.2
        
    def draw(self, surface):
        # Desenhar a teia (linha vertical)
        teia_start_y = max(0, self.start_y - 50)  # Começar um pouco acima
        pygame.draw.line(surface, self.web_color, (int(self.x), teia_start_y), (int(self.x), int(self.y)), 2)
        
        # Desenhar brilho na teia
        pygame.draw.line(surface, (255, 255, 255), (int(self.x - 1), teia_start_y), (int(self.x - 1), int(self.y)), 1)
        
        # Corpo da aranha (oval maior)
        body_size = int(self.size * 0.8)
        body_rect = pygame.Rect(self.x - body_size//2, self.y - body_size//3, body_size, body_size//1.5)
        pygame.draw.ellipse(surface, self.color, body_rect)
        
        # Contorno do corpo
        pygame.draw.ellipse(surface, (15, 5, 5), body_rect, 2)
        
        # Abdômen maior
        abdomen_size = int(self.size * 1.0)
        abdomen_rect = pygame.Rect(self.x - abdomen_size//3, self.y, abdomen_size//1.5, abdomen_size)
        pygame.draw.ellipse(surface, self.color, abdomen_rect)
        pygame.draw.ellipse(surface, (15, 5, 5), abdomen_rect, 2)
        
        # Pernas da aranha (8 pernas animadas)
        leg_length = int(self.size * 1.2)
        leg_animation = math.sin(self.animation_frame) * 5  # Movimento das pernas
        
        # Pernas esquerdas (4)
        for i in range(4):
            leg_angle = (i * 30 - 60) + leg_animation  # Ângulos das pernas com animação
            leg_end_x = self.x - leg_length * math.cos(math.radians(leg_angle))
            leg_end_y = self.y + leg_length * math.sin(math.radians(leg_angle)) * 0.3
            
            # Segmento 1 da perna
            mid_x = self.x - (leg_length * 0.6) * math.cos(math.radians(leg_angle))
            mid_y = self.y + (leg_length * 0.6) * math.sin(math.radians(leg_angle)) * 0.3
            pygame.draw.line(surface, self.leg_color, (int(self.x), int(self.y)), (int(mid_x), int(mid_y)), 3)
            
            # Segmento 2 da perna
            pygame.draw.line(surface, self.leg_color, (int(mid_x), int(mid_y)), (int(leg_end_x), int(leg_end_y)), 2)
        
        # Pernas direitas (4)
        for i in range(4):
            leg_angle = (i * 30 + 30) - leg_animation  # Ângulos das pernas com animação
            leg_end_x = self.x + leg_length * math.cos(math.radians(leg_angle))
            leg_end_y = self.y + leg_length * math.sin(math.radians(leg_angle)) * 0.3
            
            # Segmento 1 da perna
            mid_x = self.x + (leg_length * 0.6) * math.cos(math.radians(leg_angle))
            mid_y = self.y + (leg_length * 0.6) * math.sin(math.radians(leg_angle)) * 0.3
            pygame.draw.line(surface, self.leg_color, (int(self.x), int(self.y)), (int(mid_x), int(mid_y)), 3)
            
            # Segmento 2 da perna
            pygame.draw.line(surface, self.leg_color, (int(mid_x), int(mid_y)), (int(leg_end_x), int(leg_end_y)), 2)
        
        # Olhos da aranha (múltiplos olhos pequenos)
        eye_size = 2
        # Olhos principais (maiores)
        pygame.draw.circle(surface, self.eye_color, (int(self.x - 6), int(self.y - body_size//4)), eye_size + 1)
        pygame.draw.circle(surface, self.eye_color, (int(self.x + 6), int(self.y - body_size//4)), eye_size + 1)
        
        # Olhos secundários (menores)
        pygame.draw.circle(surface, self.eye_color, (int(self.x - 10), int(self.y - body_size//3)), eye_size)
        pygame.draw.circle(surface, self.eye_color, (int(self.x + 10), int(self.y - body_size//3)), eye_size)
        pygame.draw.circle(surface, self.eye_color, (int(self.x - 3), int(self.y - body_size//2)), eye_size)
        pygame.draw.circle(surface, self.eye_color, (int(self.x + 3), int(self.y - body_size//2)), eye_size)
        
        # Brilho nos olhos principais
        pygame.draw.circle(surface, (255, 150, 150), (int(self.x - 6), int(self.y - body_size//4)), 1)
        pygame.draw.circle(surface, (255, 150, 150), (int(self.x + 6), int(self.y - body_size//4)), 1)
        
        # Padrão no abdômen (marcas características)
        pattern_points = [
            (int(self.x), int(self.y + abdomen_size//3)),
            (int(self.x - 5), int(self.y + abdomen_size//2)),
            (int(self.x + 5), int(self.y + abdomen_size//2)),
            (int(self.x), int(self.y + abdomen_size//1.5))
        ]
        pygame.draw.polygon(surface, (50, 20, 20), pattern_points)
        
    def is_alive(self):
        return self.health > 0 and self.y < SCREEN_HEIGHT + 50
    
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
        self.flying_witches = []  # Lista de bruxinhas voadoras (fase 2)
        self.spiders = []  # Lista de aranhas descendo (fase 3)
        self.wizard_spawn_timer = 0
        self.bat_spawn_timer = 0
        self.flying_witch_spawn_timer = 0
        self.spider_spawn_timer = 0
        self.score = 0  # Pontuação do jogador
        self.current_phase = 1  # Fase atual (1, 2 ou 3)
        self.enemies_killed_in_phase = 0  # Inimigos mortos na fase atual
        self.enemies_needed_for_next_phase = 10  # Inimigos necessários para próxima fase
        self.enemies_needed_for_phase_3 = 10  # Inimigos necessários para fase 3
        self.enemies_needed_to_win = 15  # Inimigos necessários para ganhar a fase 3 (mais difícil)
        self.game_won = False  # Flag para indicar se o jogo foi ganho
        
        # Sistema de métricas e avaliação
        self.phase_start_time = 0  # Tempo de início da fase
        self.phase_time_limits = {1: 90, 2: 120, 3: 150}  # Segundos por fase (1.5, 2, 2.5 minutos)
        self.total_shots_fired = 0  # Total de projéteis disparados
        self.total_hits = 0  # Total de acertos
        self.damage_taken = 0  # Dano sofrido (colisões)
        self.current_combo = 0  # Combo atual de kills
        self.max_combo = 0  # Maior combo alcançado
        self.phase_times = []  # Tempos de cada fase
        self.perfect_phases = 0  # Fases completadas sem dano
        self.game_start_time = 0  # Tempo de início do jogo
        self.total_game_time = 0  # Tempo total de jogo
        
        # Carregar o background do menu
        try:
            background_path = os.path.join("..", "craftpix-671123-free-halloween-2d-game-backgrounds", 
                                         "PNG", "4_game_background", "4_game_background.png")
            menu_bg_original = pygame.image.load(background_path)
            self.menu_bg = pygame.transform.scale(menu_bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Não foi possível carregar o background. Usando cor sólida.")
            self.menu_bg = None
        
        # Carregar background do jogo
        try:
            game_bg_path = os.path.join("..", "craftpix-671123-free-halloween-2d-game-backgrounds", 
                                       "PNG", "1_game_background", "1_game_background.png")
            game_bg_original = pygame.image.load(game_bg_path)
            self.game_bg = pygame.transform.scale(game_bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Não foi possível carregar o background do jogo. Usando cor sólida.")
            self.game_bg = None
        
        # Carregar background da fase 2
        try:
            phase2_bg_path = os.path.join("..", "craftpix-671123-free-halloween-2d-game-backgrounds", 
                                        "PNG", "3_game_background", "3_game_background.png")
            phase2_bg_original = pygame.image.load(phase2_bg_path)
            self.phase2_bg = pygame.transform.scale(phase2_bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Não foi possível carregar o background da fase 2. Usando background da fase 1.")
            self.phase2_bg = self.game_bg
        
        # Carregar background da fase 3
        try:
            phase3_bg_path = os.path.join("..", "craftpix-671123-free-halloween-2d-game-backgrounds", 
                                        "PNG", "2_game_background", "2_game_background.png")
            phase3_bg_original = pygame.image.load(phase3_bg_path)
            self.phase3_bg = pygame.transform.scale(phase3_bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Não foi possível carregar o background da fase 3. Usando background da fase 1.")
            self.phase3_bg = self.game_bg
        
        # Botões do menu
        self.menu_buttons = [
            {"text": "NEW GAME", "rect": pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50, 300, 60), "action": "new_game"},
            {"text": "EXIT", "rect": pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 30, 300, 60), "action": "exit"}
        ]
        
        self.selected_button = 0
    
    def draw_dripping_text(self, surface, text, font, x, y, main_color, drip_color):
        """Desenha texto com efeito de gotejamento simples"""
        # Renderizar o texto principal
        text_surface = font.render(text, True, main_color)
        text_rect = text_surface.get_rect(center=(x, y))
        
        # Desenhar o texto principal
        surface.blit(text_surface, text_rect)
        
        return text_rect
    
    def draw_gothic_title(self, surface, text, x, y):
        """Desenha título com efeito gótico simples"""
        # Renderizar o texto com a fonte especial
        title_surface = font_title.render(text, True, (255, 180, 60))  # Laranja
        title_rect = title_surface.get_rect(center=(x, y))
        
        # Sombra simples
        shadow_surface = font_title.render(text, True, (100, 50, 0))  # Marrom escuro
        shadow_rect = shadow_surface.get_rect(center=(x + 3, y + 3))
        
        # Desenhar sombra primeiro
        surface.blit(shadow_surface, shadow_rect)
        
        # Desenhar texto principal
        surface.blit(title_surface, title_rect)
        
        return title_rect
    
    def get_accuracy_percentage(self):
        """Calcula porcentagem de precisão"""
        if self.total_shots_fired == 0:
            return 0
        return (self.total_hits / self.total_shots_fired) * 100
    
    def get_time_bonus(self, phase_number):
        """Calcula bonus de tempo para uma fase"""
        if phase_number > len(self.phase_times):
            return 0
        
        phase_time = self.phase_times[phase_number - 1]
        time_limit = self.phase_time_limits[phase_number]
        
        if phase_time <= time_limit * 0.5:  # Muito rápido (50% do tempo)
            return 1000
        elif phase_time <= time_limit * 0.7:  # Rápido (70% do tempo)
            return 500
        elif phase_time <= time_limit * 0.9:  # Bom tempo (90% do tempo)
            return 200
        else:
            return 0
    
    def calculate_final_score(self):
        """Calcula pontuação final com todos os bônus"""
        base_score = self.score
        
        # Bônus de precisão
        accuracy = self.get_accuracy_percentage()
        accuracy_bonus = int(accuracy * 10)  # 10 pontos por % de precisão
        
        # Bônus de tempo de todas as fases
        time_bonus = sum(self.get_time_bonus(i) for i in range(1, len(self.phase_times) + 1))
        
        # Bônus de combo
        combo_bonus = self.max_combo * 50
        
        # Bônus de fases perfeitas (sem dano)
        perfect_bonus = self.perfect_phases * 500
        
        # Penalty por dano recebido
        damage_penalty = self.damage_taken * 25
        
        final_score = base_score + accuracy_bonus + time_bonus + combo_bonus + perfect_bonus - damage_penalty
        return max(0, final_score)  # Não permitir score negativo
    
    def get_performance_rating(self):
        """Calcula avaliação de performance baseada em múltiplas métricas"""
        accuracy = self.get_accuracy_percentage()
        avg_time_performance = 0
        
        # Calcular performance média de tempo
        if self.phase_times:
            total_time_performance = 0
            for i, phase_time in enumerate(self.phase_times, 1):
                time_limit = self.phase_time_limits[i]
                time_performance = max(0, 100 - (phase_time / time_limit) * 100)
                total_time_performance += time_performance
            avg_time_performance = total_time_performance / len(self.phase_times)
        
        # Calcular performance de dano (menos dano = melhor)
        damage_performance = max(0, 100 - (self.damage_taken * 10))  # Cada hit = -10%
        
        # Calcular performance de combo
        combo_performance = min(100, self.max_combo * 5)  # Cada combo = +5%
        
        # Performance geral (média ponderada)
        overall_performance = (
            accuracy * 0.3 +           # 30% precisão
            avg_time_performance * 0.25 +  # 25% tempo
            damage_performance * 0.25 +     # 25% resistência
            combo_performance * 0.2         # 20% combo
        )
        
        # Definir classificações
        if overall_performance >= 95:
            return "LENDÁRIO", "🏆", "MESTRE DAS TREVAS SUPREMO!"
        elif overall_performance >= 85:
            return "ÉPICO", "⭐", "GUERREIRO SOMBRIO ÉPICO!"
        elif overall_performance >= 75:
            return "ÓTIMO", "🔥", "CAÇADOR HABILIDOSO!"
        elif overall_performance >= 65:
            return "BOM", "👍", "APRENDIZ VALENTE!"
        elif overall_performance >= 50:
            return "REGULAR", "😐", "PRECISA TREINAR MAIS..."
        else:
            return "PÉSSIMO", "💀", "AS TREVAS TE VENCERAM..."
    
    def get_detailed_stats(self):
        """Retorna estatísticas detalhadas para exibição"""
        stats = {
            'accuracy': self.get_accuracy_percentage(),
            'total_time': sum(self.phase_times) if self.phase_times else 0,
            'max_combo': self.max_combo,
            'damage_taken': self.damage_taken,
            'perfect_phases': self.perfect_phases,
            'shots_fired': self.total_shots_fired,
            'hits': self.total_hits,
            'final_score': self.calculate_final_score()
        }
        return stats
    
    def toggle_fullscreen(self):
        """Alternar entre tela cheia e janela"""
        global screen, SCREEN_WIDTH, SCREEN_HEIGHT
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # Tela cheia usando a resolução nativa
            screen = pygame.display.set_mode((NATIVE_WIDTH, NATIVE_HEIGHT), pygame.FULLSCREEN)
            # Recalcular resolução para tela cheia
            SCREEN_WIDTH = NATIVE_WIDTH
            SCREEN_HEIGHT = NATIVE_HEIGHT
        else:
            # Janela menor mantendo proporção
            window_width = min(1024, NATIVE_WIDTH - 100)
            window_height = int(window_width * 9 / 16)
            screen = pygame.display.set_mode((window_width, window_height))
            SCREEN_WIDTH = window_width
            SCREEN_HEIGHT = window_height
    
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
            self.flying_witches = []
            self.spiders = []
            self.wizard_spawn_timer = 0
            self.bat_spawn_timer = 0
            self.flying_witch_spawn_timer = 0
            self.spider_spawn_timer = 0
            self.score = 0
            self.current_phase = 1
            self.enemies_killed_in_phase = 0
            self.game_won = False
            
            # Resetar métricas
            self.phase_start_time = pygame.time.get_ticks()
            self.game_start_time = pygame.time.get_ticks()
            self.total_shots_fired = 0
            self.total_hits = 0
            self.damage_taken = 0
            self.current_combo = 0
            self.max_combo = 0
            self.phase_times = []
            self.perfect_phases = 0
            self.total_game_time = 0
            
            # Criar apenas um mago Fire Vizard no canto esquerdo da tela
            spawn_x = 100  # Posição no canto esquerdo
            spawn_y = SCREEN_HEIGHT - 200  # Bem à frente do cenário
            self.wizards.append(Wizard(spawn_x, spawn_y, "fire"))
            print("Iniciando novo jogo - Fase 1...")
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
            # Redimensionar para tela atual se necessário
            if self.menu_bg.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                self.menu_bg = pygame.transform.scale(self.menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            # Desenhar a primeira imagem
            screen.blit(self.menu_bg, (self.bg_x, 0))
            # Desenhar a segunda imagem para criar o efeito infinito
            screen.blit(self.menu_bg, (self.bg_x + SCREEN_WIDTH, 0))
        else:
            # Fundo com gradiente atmosférico simples
            for y in range(0, SCREEN_HEIGHT, 3):
                intensity = y / SCREEN_HEIGHT
                r = int(30 + intensity * 50)
                g = int(15 + intensity * 30)
                b = int(80 + intensity * 100)
                pygame.draw.rect(screen, (r, g, b), (0, y, SCREEN_WIDTH, 3))
        
        # Desenhar brasas atrás do conteúdo do menu
        for ember in self.embers:
            ember.draw(screen)
        
        # Título do jogo simples
        self.draw_gothic_title(screen, "HALLOWEEN", SCREEN_WIDTH//2, SCREEN_HEIGHT//4 - 20)
        
        # Subtítulo simples
        subtitle_color = (200, 100, 30)  # Laranja escuro
        self.draw_dripping_text(screen, "GAME", font_medium, SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 60, 
                               subtitle_color, (120, 50, 10))
        
        # Desenhar botões simples
        for i, button in enumerate(self.menu_buttons):
            # Cores do botão (destacado se selecionado)
            if i == self.selected_button:
                button_color = (255, 100, 0)  # Laranja mais intenso
                text_color = BLACK
                border_color = (255, 255, 100)  # Amarelo brilhante
                glow_color = (255, 200, 0)  # Brilho dourado
            else:
                button_color = (150, 50, 0)  # Laranja escuro
                text_color = (200, 200, 200)  # Cinza claro
                border_color = (100, 30, 0)  # Marrom escuro
                glow_color = None
            
            # Efeito de brilho ao redor do botão selecionado
            if i == self.selected_button:
                glow_rect = pygame.Rect(button["rect"].x - 5, button["rect"].y - 5, 
                                      button["rect"].width + 10, button["rect"].height + 10)
                pygame.draw.rect(screen, glow_color, glow_rect)
                pygame.draw.rect(screen, (255, 255, 0), glow_rect, 2)
            
            # Sombra do botão
            shadow_rect = pygame.Rect(button["rect"].x + 3, button["rect"].y + 3,
                                    button["rect"].width, button["rect"].height)
            pygame.draw.rect(screen, (20, 10, 0), shadow_rect)
            
            # Desenhar retângulo do botão
            pygame.draw.rect(screen, button_color, button["rect"])
            pygame.draw.rect(screen, border_color, button["rect"], 4)
            
            # Gradiente interno para dar profundidade
            inner_rect = pygame.Rect(button["rect"].x + 5, button["rect"].y + 5,
                                   button["rect"].width - 10, button["rect"].height - 10)
            inner_color = tuple(min(255, c + 30) for c in button_color)
            pygame.draw.rect(screen, inner_color, inner_rect)
            
            # Desenhar texto do botão com efeito
            button_text = font_medium.render(button["text"], True, text_color)
            text_rect = button_text.get_rect(center=button["rect"].center)
            
            # Sombra do texto
            text_shadow = font_medium.render(button["text"], True, (50, 25, 0))
            shadow_text_rect = text_shadow.get_rect(center=(button["rect"].centerx + 2, button["rect"].centery + 2))
            screen.blit(text_shadow, shadow_text_rect)
            
            # Texto principal
            screen.blit(button_text, text_rect)
        
        # Instruções menores e mais embaixo
        instruction_text = font_tiny.render("Use as setas ou mouse para navegar", True, (150, 150, 150))
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 60))
        screen.blit(instruction_text, instruction_rect)
        
        enter_text = font_tiny.render("ENTER/ESPAÇO para selecionar | ESC para sair | F11 para tela cheia", True, (150, 150, 150))
        enter_rect = enter_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 40))
        screen.blit(enter_text, enter_rect)
        
        # Texto decorativo adicional
        subtitle_text = font_small.render("~ Uma Aventura Macabra ~", True, (200, 100, 50))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 80))
        screen.blit(subtitle_text, subtitle_rect)
    
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
                            # Contar tiro disparado
                            self.total_shots_fired += 1
                            
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
        # Verificar tempo limite da fase
        current_time = (pygame.time.get_ticks() - self.phase_start_time) / 1000
        time_limit = self.phase_time_limits[self.current_phase]
        
        if current_time >= time_limit:
            # Tempo esgotado! Game Over
            print(f"Tempo esgotado na Fase {self.current_phase}!")
            self.state = GameState.MENU  # Voltar ao menu
            return
        
        # Atualizar magos existentes
        for wizard in self.wizards[:]:
            wizard.update()  # Não mais atirar automaticamente
        
        # Atualizar projéteis
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.is_alive():
                self.projectiles.remove(projectile)
        
        # Lógica específica por fase
        if self.current_phase == 1:
            # FASE 1: Morcegos
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
                        self.enemies_killed_in_phase += 1
                        
                        # Atualizar métricas
                        self.total_hits += 1
                        self.current_combo += 1
                        self.max_combo = max(self.max_combo, self.current_combo)
                        break
            
            # Spawnar novos morcegos
            self.bat_spawn_timer += 1
            if self.bat_spawn_timer >= 120:  # Novo morcego a cada 2 segundos
                # Spawnar morcegos do lado direito da tela
                spawn_x = SCREEN_WIDTH + 50
                spawn_y = random.randint(100, SCREEN_HEIGHT - 100)
                # Passar o mago como alvo para o morcego
                target_wizard = self.wizards[0] if self.wizards else None
                new_bat = Bat(spawn_x, spawn_y, target_wizard)
                # Aumentar um pouco a velocidade do morcego na direção do mago
                new_bat.tracking_speed = 1.5
                self.bats.append(new_bat)
                self.bat_spawn_timer = 0
            
            # Limitar número de morcegos para performance
            if len(self.bats) > 10:
                self.bats = self.bats[-8:]  # Manter apenas os 8 mais recentes
            
            # Verificar se deve passar para a fase 2
            if self.enemies_killed_in_phase >= self.enemies_needed_for_next_phase:
                self.advance_to_phase_2()
            
            # Verificar colisões entre mago e morcegos (dano)
            if self.wizards:
                wizard = self.wizards[0]
                wizard_rect = pygame.Rect(wizard.x - 40, wizard.y - 40, 80, 80)
                for bat in self.bats[:]:
                    bat_rect = bat.get_rect()
                    if wizard_rect.colliderect(bat_rect):
                        self.damage_taken += 1
                        self.current_combo = 0  # Reset combo ao levar dano
                        self.bats.remove(bat)  # Remove o morcego após collision
                        break
                
        elif self.current_phase == 2:
            # FASE 2: Bruxinhas voadoras (mais rápida)
            # Atualizar bruxinhas
            for flying_witch in self.flying_witches[:]:
                flying_witch.update()
                if not flying_witch.is_alive():
                    self.flying_witches.remove(flying_witch)
            
            # Verificar colisões entre projéteis e bruxinhas
            for projectile in self.projectiles[:]:
                projectile_rect = pygame.Rect(projectile.x - projectile.size, projectile.y - projectile.size, 
                                            projectile.size * 2, projectile.size * 2)
                for flying_witch in self.flying_witches[:]:
                    witch_rect = flying_witch.get_rect()
                    if projectile_rect.colliderect(witch_rect):
                        # Colisão detectada!
                        self.flying_witches.remove(flying_witch)
                        self.projectiles.remove(projectile)
                        self.score += 15  # Mais pontos por bruxa
                        self.enemies_killed_in_phase += 1
                        
                        # Atualizar métricas
                        self.total_hits += 1
                        self.current_combo += 1
                        self.max_combo = max(self.max_combo, self.current_combo)
                        break
            
            # Spawnar novas bruxinhas (mais rápido na fase 2)
            self.flying_witch_spawn_timer += 1
            if self.flying_witch_spawn_timer >= 90:  # Nova bruxa a cada 1.5 segundos (mais rápido)
                # Spawnar bruxinhas do lado direito da tela
                spawn_x = SCREEN_WIDTH + 50
                spawn_y = random.randint(80, SCREEN_HEIGHT - 80)
                # Passar o mago como alvo para a bruxa
                target_wizard = self.wizards[0] if self.wizards else None
                new_witch = FlyingWitch(spawn_x, spawn_y, target_wizard)
                # Aumentar velocidade na fase 2
                new_witch.tracking_speed = 1.2  # Mais rápida
                self.flying_witches.append(new_witch)
                self.flying_witch_spawn_timer = 0
            
            # Limitar número de bruxinhas para performance
            if len(self.flying_witches) > 8:
                self.flying_witches = self.flying_witches[-6:]  # Manter apenas as 6 mais recentes
            
            # Verificar se deve passar para a fase 3
            if self.enemies_killed_in_phase >= self.enemies_needed_for_phase_3:
                self.advance_to_phase_3()
            
            # Verificar colisões entre mago e bruxinhas (dano)
            if self.wizards:
                wizard = self.wizards[0]
                wizard_rect = pygame.Rect(wizard.x - 40, wizard.y - 40, 80, 80)
                for flying_witch in self.flying_witches[:]:
                    witch_rect = flying_witch.get_rect()
                    if wizard_rect.colliderect(witch_rect):
                        self.damage_taken += 1
                        self.current_combo = 0  # Reset combo ao levar dano
                        self.flying_witches.remove(flying_witch)  # Remove a bruxa após collision
                        break
                
        elif self.current_phase == 3:
            # FASE 3: Aranhas descendo nas teias (mais difícil e rápida)
            # Atualizar aranhas
            for spider in self.spiders[:]:
                spider.update()
                if not spider.is_alive():
                    self.spiders.remove(spider)
            
            # Verificar colisões entre projéteis e aranhas
            for projectile in self.projectiles[:]:
                projectile_rect = pygame.Rect(projectile.x - projectile.size, projectile.y - projectile.size, 
                                            projectile.size * 2, projectile.size * 2)
                for spider in self.spiders[:]:
                    spider_rect = spider.get_rect()
                    if projectile_rect.colliderect(spider_rect):
                        # Colisão detectada!
                        self.spiders.remove(spider)
                        self.projectiles.remove(projectile)
                        self.score += 20  # Mais pontos por aranha (mais difícil)
                        self.enemies_killed_in_phase += 1
                        
                        # Atualizar métricas
                        self.total_hits += 1
                        self.current_combo += 1
                        self.max_combo = max(self.max_combo, self.current_combo)
                        break
            
            # Spawnar novas aranhas (mais rápido na fase 3 - mais difícil)
            self.spider_spawn_timer += 1
            if self.spider_spawn_timer >= 60:  # Nova aranha a cada 1 segundo (mais rápido)
                # Spawnar aranhas do topo da tela
                spawn_x = random.randint(100, SCREEN_WIDTH - 100)
                spawn_y = 50  # Começar do topo
                new_spider = Spider(spawn_x, spawn_y)
                # Aumentar velocidade na fase 3 (mais difícil)
                new_spider.vel_y = random.uniform(2.5, 4.0)  # Descida mais rápida
                self.spiders.append(new_spider)
                self.spider_spawn_timer = 0
            
            # Limitar número de aranhas para performance
            if len(self.spiders) > 12:  # Mais aranhas na tela (mais difícil)
                self.spiders = self.spiders[-10:]  # Manter apenas as 10 mais recentes
            
            # Verificar se o jogo foi ganho
            if self.enemies_killed_in_phase >= self.enemies_needed_to_win:
                self.game_won = True
                # Calcular tempo total do jogo
                self.total_game_time = (pygame.time.get_ticks() - self.game_start_time) / 1000
            
            # Verificar colisões entre mago e aranhas (dano)
            if self.wizards:
                wizard = self.wizards[0]
                wizard_rect = pygame.Rect(wizard.x - 40, wizard.y - 40, 80, 80)
                for spider in self.spiders[:]:
                    spider_rect = spider.get_rect()
                    if wizard_rect.colliderect(spider_rect):
                        self.damage_taken += 1
                        self.current_combo = 0  # Reset combo ao levar dano
                        self.spiders.remove(spider)  # Remove a aranha após collision
                        break
    
    def advance_to_phase_2(self):
        """Avança para a fase 2"""
        # Registrar tempo da fase 1
        phase_time = (pygame.time.get_ticks() - self.phase_start_time) / 1000
        self.phase_times.append(phase_time)
        
        # Verificar se fase foi perfeita (sem dano)
        if self.damage_taken == 0:
            self.perfect_phases += 1
        
        print(f"Fase 1 completada em {phase_time:.1f} segundos!")
        print("Avançando para a Fase 2!")
        
        self.current_phase = 2
        self.enemies_killed_in_phase = 0
        self.phase_start_time = pygame.time.get_ticks()  # Reset timer para nova fase
        
        # Limpar inimigos da fase anterior
        self.bats.clear()
        
        # Trocar o mago para Wanderer com magic_arrow
        if self.wizards:
            wizard_pos = (self.wizards[0].x, self.wizards[0].y)
            self.wizards.clear()
            self.wizards.append(Wizard(wizard_pos[0], wizard_pos[1], "wanderer"))
            print("Mago mudou para Wanderer com Magic Arrow!")
            print("Agora enfrentando Bruxinhas Voadoras!")
    
    def advance_to_phase_3(self):
        """Avança para a fase 3"""
        # Registrar tempo da fase 2
        phase_time = (pygame.time.get_ticks() - self.phase_start_time) / 1000
        self.phase_times.append(phase_time)
        
        # Verificar se fase foi perfeita (sem dano na fase atual)
        current_damage = self.damage_taken
        if len(self.phase_times) == 2:  # Estamos na transição da fase 2 para 3
            # Considerar perfeita se não houve dano adicional nesta fase
            if current_damage <= 1:  # Permitir até 1 dano na fase 2
                self.perfect_phases += 1
        
        print(f"Fase 2 completada em {phase_time:.1f} segundos!")
        print("Avançando para a Fase 3!")
        
        self.current_phase = 3
        self.enemies_killed_in_phase = 0
        self.phase_start_time = pygame.time.get_ticks()  # Reset timer para nova fase
        
        # Limpar inimigos da fase anterior
        self.flying_witches.clear()
        
        # Trocar o mago para espada (Attack_2.png)
        if self.wizards:
            wizard_pos = (self.wizards[0].x, self.wizards[0].y)
            self.wizards.clear()
            self.wizards.append(Wizard(wizard_pos[0], wizard_pos[1], "sword"))
            print("Mago mudou para Espada (Attack_2)!")
            print("Agora enfrentando Aranhas descendo nas Teias!")
            print("Fase mais difícil - prepare-se!")
    
    def draw_game(self):
        # Desenhar background baseado na fase (redimensionado para a tela atual)
        if self.current_phase == 1:
            if self.game_bg:
                # Redimensionar para tela atual se necessário
                if self.game_bg.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                    self.game_bg = pygame.transform.scale(self.game_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(self.game_bg, (0, 0))
            else:
                screen.fill((30, 15, 60))  # Fundo roxo escuro
        elif self.current_phase == 2:
            if self.phase2_bg:
                # Redimensionar para tela atual se necessário
                if self.phase2_bg.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                    self.phase2_bg = pygame.transform.scale(self.phase2_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(self.phase2_bg, (0, 0))
            else:
                screen.fill((60, 30, 15))  # Fundo marrom escuro
        else:  # Fase 3
            if self.phase3_bg:
                # Redimensionar para tela atual se necessário
                if self.phase3_bg.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                    self.phase3_bg = pygame.transform.scale(self.phase3_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(self.phase3_bg, (0, 0))
            else:
                screen.fill((15, 30, 60))  # Fundo azul escuro
        
        # Atualizar lógica do jogo
        self.update_game()
        
        # Desenhar magos
        for wizard in self.wizards:
            wizard.draw(screen)
        
        # Desenhar projéteis
        for projectile in self.projectiles:
            projectile.draw(screen)
        
        # Desenhar inimigos baseado na fase
        if self.current_phase == 1:
            # Desenhar morcegos
            for bat in self.bats:
                bat.draw(screen)
        elif self.current_phase == 2:
            # Desenhar bruxinhas voadoras
            for flying_witch in self.flying_witches:
                flying_witch.draw(screen)
        else:  # Fase 3
            # Desenhar aranhas descendo
            for spider in self.spiders:
                spider.draw(screen)
        
        # UI do jogo
        # Informações da fase
        phase_text = font_medium.render(f"FASE {self.current_phase}", True, YELLOW)
        screen.blit(phase_text, (SCREEN_WIDTH//2 - 50, 10))
        
        # Tempo restante da fase
        current_time = (pygame.time.get_ticks() - self.phase_start_time) / 1000
        time_limit = self.phase_time_limits[self.current_phase]
        time_remaining = max(0, time_limit - current_time)
        
        time_color = WHITE
        if time_remaining < 30:  # Últimos 30 segundos
            time_color = RED if int(time_remaining) % 2 == 0 else YELLOW  # Piscar
        elif time_remaining < 60:  # Último minuto
            time_color = ORANGE
        
        time_text = font_small.render(f"Tempo: {time_remaining:.1f}s", True, time_color)
        screen.blit(time_text, (SCREEN_WIDTH//2 - 50, 50))
        
        # Progresso da fase
        if self.current_phase == 1:
            progress_text = font_small.render(f"Morcegos: {self.enemies_killed_in_phase}/{self.enemies_needed_for_next_phase}", True, WHITE)
        elif self.current_phase == 2:
            progress_text = font_small.render(f"Bruxinhas: {self.enemies_killed_in_phase}/{self.enemies_needed_for_phase_3}", True, WHITE)
        else:  # Fase 3
            progress_text = font_small.render(f"Aranhas: {self.enemies_killed_in_phase}/{self.enemies_needed_to_win}", True, WHITE)
        screen.blit(progress_text, (SCREEN_WIDTH//2 - 100, 80))
        
        # Estatísticas em tempo real (lado esquerdo)
        real_time_stats = [
            f"Score: {self.score}",
            f"Combo: {self.current_combo}x",
            f"Precisão: {self.get_accuracy_percentage():.1f}%",
            f"Dano: {self.damage_taken}"
        ]
        
        for i, stat in enumerate(real_time_stats):
            color = WHITE
            if "Combo" in stat and self.current_combo > 5:
                color = YELLOW
            elif "Precisão" in stat:
                accuracy = self.get_accuracy_percentage()
                if accuracy >= 80:
                    color = (100, 255, 100)  # Verde
                elif accuracy >= 60:
                    color = YELLOW
                else:
                    color = RED
            
            stat_surface = font_small.render(stat, True, color)
            screen.blit(stat_surface, (10, 10 + i * 25))
        
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
        
        # Tela de vitória
        if self.game_won:
            # Registrar tempo da fase 3 se ainda não foi registrado
            if len(self.phase_times) == 2:
                phase_time = (pygame.time.get_ticks() - self.phase_start_time) / 1000
                self.phase_times.append(phase_time)
                print(f"Fase 3 completada em {phase_time:.1f} segundos!")
            
            # Overlay semi-transparente
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Obter avaliação e estatísticas
            rating, icon, message = self.get_performance_rating()
            stats = self.get_detailed_stats()
            
            # Título de vitória com rating
            victory_text = font_large.render(f"{icon} {rating} {icon}", True, YELLOW)
            victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 200))
            screen.blit(victory_text, victory_rect)
            
            # Mensagem personalizada
            message_text = font_medium.render(message, True, ORANGE)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
            screen.blit(message_text, message_rect)
            
            # Estatísticas detalhadas (lado esquerdo)
            stats_y = SCREEN_HEIGHT//2 - 100
            stats_left = SCREEN_WIDTH//4
            
            stat_texts = [
                f"Pontuação Final: {stats['final_score']:,}",
                f"Precisão: {stats['accuracy']:.1f}%",
                f"Tempo Total: {stats['total_time']:.1f}s",
                f"Maior Combo: {stats['max_combo']}x",
                f"Dano Recebido: {stats['damage_taken']} hits"
            ]
            
            for i, text in enumerate(stat_texts):
                color = WHITE if i != 0 else YELLOW  # Primeira linha (score) em amarelo
                stat_surface = font_small.render(text, True, color)
                screen.blit(stat_surface, (stats_left - 150, stats_y + i * 30))
            
            # Estatísticas adicionais (lado direito)
            stats_right = 3 * SCREEN_WIDTH//4
            
            additional_stats = [
                f"Tiros Disparados: {stats['shots_fired']}",
                f"Acertos: {stats['hits']}",
                f"Fases Perfeitas: {stats['perfect_phases']}/3",
                f"Tempo Fase 1: {self.phase_times[0]:.1f}s" if len(self.phase_times) > 0 else "Fase 1: --",
                f"Tempo Fase 2: {self.phase_times[1]:.1f}s" if len(self.phase_times) > 1 else "Fase 2: --"
            ]
            
            if len(self.phase_times) > 2:
                additional_stats.append(f"Tempo Fase 3: {self.phase_times[2]:.1f}s")
            
            for i, text in enumerate(additional_stats):
                stat_surface = font_small.render(text, True, WHITE)
                screen.blit(stat_surface, (stats_right - 150, stats_y + i * 30))
            
            # Bônus detalhados
            bonus_y = SCREEN_HEIGHT//2 + 80
            bonus_texts = [
                "=== BÔNUS OBTIDOS ===",
                f"Precisão: +{int(stats['accuracy'] * 10)}",
                f"Tempo: +{sum(self.get_time_bonus(i) for i in range(1, len(self.phase_times) + 1))}",
                f"Combo: +{stats['max_combo'] * 50}",
                f"Fases Perfeitas: +{stats['perfect_phases'] * 500}",
                f"Penalty Dano: -{stats['damage_taken'] * 25}"
            ]
            
            for i, text in enumerate(bonus_texts):
                color = YELLOW if i == 0 else WHITE
                if "Penalty" in text:
                    color = RED
                elif "+" in text and i > 0:
                    color = (100, 255, 100)  # Verde para bônus
                    
                bonus_surface = font_tiny.render(text, True, color)
                bonus_rect = bonus_surface.get_rect(center=(SCREEN_WIDTH//2, bonus_y + i * 20))
                screen.blit(bonus_surface, bonus_rect)
            
            # Instruções
            instruction_text = font_small.render("Pressione ESC para voltar ao menu", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
            screen.blit(instruction_text, instruction_rect)
    
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