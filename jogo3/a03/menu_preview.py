#!/usr/bin/env python3
"""
Preview das melhorias visuais do menu Halloween
"""
import pygame
import sys
import os
import math
import random

# Inicializar pygame
pygame.init()

# Configurar tela pequena para preview
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Halloween Game - Menu Preview")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 100)

# Fontes
try:
    font_title_mega = pygame.font.SysFont('chiller', 120)
    font_medium = pygame.font.SysFont('chiller', 40)
    font_small = pygame.font.SysFont('arial', 20)
    print("✓ Fontes carregadas com sucesso!")
except:
    font_title_mega = pygame.font.Font(None, 120)
    font_medium = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 20)
    print("✓ Fontes padrão carregadas!")

def draw_dripping_text(surface, text, font, x, y, main_color, drip_color):
    """Desenha texto com efeito de gotejamento"""
    text_surface = font.render(text, True, main_color)
    text_rect = text_surface.get_rect(center=(x, y))
    
    # Criar efeito de gotejamento
    drip_surface = pygame.Surface((text_rect.width + 80, text_rect.height + 120), pygame.SRCALPHA)
    
    current_time = pygame.time.get_ticks()
    
    # Desenhar gotas
    for i in range(15):
        drip_x = (i * 31) % text_rect.width
        drip_base_height = 15 + (i * 11) % 30
        animation_offset = math.sin(current_time * 0.003 + i) * 3
        drip_height = drip_base_height + animation_offset
        
        # Gota principal
        pygame.draw.ellipse(drip_surface, drip_color, 
                          (drip_x, text_rect.height + 5, 3, drip_height))
        
        # Gota na ponta
        pygame.draw.circle(drip_surface, drip_color, 
                         (int(drip_x + 1.5), int(text_rect.height + drip_height + 5)), 2)
    
    # Desenhar as gotas primeiro
    surface.blit(drip_surface, (text_rect.x - 40, text_rect.y))
    
    # Desenhar o texto principal
    surface.blit(text_surface, text_rect)
    
    return text_rect

def draw_gothic_title(surface, text, x, y):
    """Desenha título gótico com efeitos"""
    # Pulsação
    pulse = math.sin(pygame.time.get_ticks() * 0.005) * 0.2 + 1.0
    
    # Sombras múltiplas
    shadow_colors = [(80, 0, 0), (60, 0, 0), (40, 0, 0), (20, 0, 0)]
    shadow_offsets = [(15, 15), (10, 10), (6, 6), (3, 3)]
    
    # Desenhar sombras
    for shadow_color, offset in zip(shadow_colors, shadow_offsets):
        shadow_x = x + offset[0]
        shadow_y = y + offset[1]
        draw_dripping_text(surface, text, font_title_mega, shadow_x, shadow_y, 
                         shadow_color, (shadow_color[0]//2, 0, 0))
    
    # Texto principal
    main_color = (255, int(200 * pulse), int(80 * pulse))
    drip_color = (180, int(60 * pulse), 0)
    
    title_rect = draw_dripping_text(surface, text, font_title_mega, x, y, main_color, drip_color)
    
    # Partículas ao redor
    current_time = pygame.time.get_ticks()
    for i in range(8):
        angle = (current_time * 0.001 + i * 0.8) % (2 * math.pi)
        distance = 80 + math.sin(current_time * 0.002 + i) * 20
        
        particle_x = x + math.cos(angle) * distance
        particle_y = y + math.sin(angle) * distance
        
        particle_size = 2 + abs(math.sin(current_time * 0.003 + i)) * 2
        particle_color = (255, int(150 + math.sin(current_time * 0.004 + i) * 100), 0)
        
        pygame.draw.circle(surface, particle_color, 
                         (int(particle_x), int(particle_y)), int(particle_size))
    
    return title_rect

def main():
    clock = pygame.time.Clock()
    running = True
    
    print("🎃 HALLOWEEN GAME - MENU PREVIEW 🎃")
    print("Pressione ESC para sair")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Limpar tela
        screen.fill(BLACK)
        
        # Fundo gradiente
        current_time = pygame.time.get_ticks()
        for y in range(0, SCREEN_HEIGHT, 4):
            intensity = y / SCREEN_HEIGHT
            r = int(30 + intensity * 40)
            g = int(15 + intensity * 20)
            b = int(60 + intensity * 80)
            
            pulse = math.sin(current_time * 0.002 + y * 0.01) * 10
            r = max(0, min(255, r + pulse))
            g = max(0, min(255, g + pulse * 0.3))
            b = max(0, min(255, b + pulse * 0.5))
            
            pygame.draw.rect(screen, (r, g, b), (0, y, SCREEN_WIDTH, 4))
        
        # Título gótico
        draw_gothic_title(screen, "HALLOWEEN", SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
        
        # Subtítulo
        draw_dripping_text(screen, "GAME", font_medium, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 
                         (220, 120, 40), (140, 60, 20))
        
        # Instruções
        info_text = font_small.render("Preview das Melhorias Visuais - ESC para sair", True, WHITE)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        screen.blit(info_text, info_rect)
        
        # Atualizar tela
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("✓ Preview concluído!")

if __name__ == "__main__":
    main()
