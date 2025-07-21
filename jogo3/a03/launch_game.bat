@echo off
title Halloween Game Launcher
echo.
echo 🎃 HALLOWEEN GAME - LAUNCHER 🎃
echo.
echo Verificando Python e Pygame...
python -c "import pygame; print('✓ Pygame está instalado!')" 2>nul
if errorlevel 1 (
    echo.
    echo ❌ Pygame não está instalado!
    echo Execute: pip install pygame
    pause
    exit /b 1
)

echo ✓ Pygame funcionando!
echo.
echo 🎮 CONTROLES DO JOGO:
echo   Menu: Setas ↑↓ ou Mouse para navegar
echo   Menu: ENTER/ESPAÇO para selecionar
echo   Jogo: Seta → para atirar
echo   Jogo: Setas ↑↓ para pular
echo   ESC para sair ^| F11 para tela cheia
echo.
echo Iniciando o jogo em 3 segundos...
timeout /t 3 >nul
cls

python jogo.py

if errorlevel 1 (
    echo.
    echo ❌ Erro ao executar o jogo!
    echo Verifique se todos os arquivos estão presentes.
    echo.
    pause
) else (
    echo.
    echo 🎃 Jogo finalizado com sucesso!
    echo Obrigado por jogar Halloween Game!
    echo.
)

pause
