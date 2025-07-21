#!/usr/bin/env python3
"""
Script para executar o Halloween Game
"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🎃 INICIANDO HALLOWEEN GAME 🎃")
    print("Carregando jogo...")
    
    # Importar e executar o jogo
    from jogo import Game
    
    print("✓ Jogo carregado com sucesso!")
    print("🎮 Controles:")
    print("  - Menu: Setas ↑↓ ou Mouse para navegar")
    print("  - Menu: ENTER/ESPAÇO para selecionar")
    print("  - Jogo: Seta → para atirar")
    print("  - Jogo: Setas ↑↓ para pular")
    print("  - ESC para sair | F11 para tela cheia")
    print("")
    print("🎃 BOA SORTE! 🎃")
    print("")
    
    # Criar e executar o jogo
    game = Game()
    game.run()
    
except KeyboardInterrupt:
    print("\n🎃 Jogo interrompido pelo usuário!")
except Exception as e:
    print(f"\n❌ Erro ao executar o jogo: {e}")
    import traceback
    traceback.print_exc()
    input("\nPressione ENTER para sair...")
finally:
    print("✓ Halloween Game finalizado!")
