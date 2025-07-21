#!/usr/bin/env python3
"""
Teste rápido das melhorias implementadas
"""
import pygame
import sys
import os

# Verificar se o jogo pode ser importado sem erros
try:
    print("Testando importação do jogo...")
    
    # Adicionar o diretório do jogo ao path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Tentar importar as classes do jogo
    from jogo import Game, GameState, Wizard, Projectile, Bat, FlyingWitch, Spider
    
    print("✓ Todas as classes foram importadas com sucesso!")
    
    # Testar inicialização do pygame
    pygame.init()
    print("✓ Pygame inicializado com sucesso!")
    
    # Testar criação do jogo
    game = Game()
    print("✓ Jogo criado com sucesso!")
    
    # Testar algumas funções específicas
    print("\nTestando funcionalidades específicas:")
    
    # Testar cálculo de precisão
    game.total_shots_fired = 10
    game.total_hits = 8
    accuracy = game.get_accuracy_percentage()
    print(f"✓ Cálculo de precisão: {accuracy:.1f}%")
    
    # Testar avaliação de performance
    rating, icon, message = game.get_performance_rating()
    print(f"✓ Avaliação de performance: {rating} {icon} - {message}")
    
    # Testar estatísticas detalhadas
    stats = game.get_detailed_stats()
    print(f"✓ Estatísticas detalhadas: {len(stats)} métricas")
    
    print("\n🎃 TESTE CONCLUÍDO COM SUCESSO! 🎃")
    print("Todas as melhorias estão funcionando corretamente.")
    print("Execute 'python jogo.py' para jogar!")
    
except Exception as e:
    print(f"❌ Erro durante o teste: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
