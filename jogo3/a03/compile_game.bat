@echo off
echo.
echo 🎃 COMPILADOR DO HALLOWEEN GAME 🎃
echo.
echo Iniciando compilacao do jogo...
echo.

REM Verificar se o PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller nao encontrado! Instalando...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Erro ao instalar PyInstaller!
        pause
        exit /b 1
    )
)

echo ✓ PyInstaller encontrado!
echo.

REM Limpar builds anteriores
if exist "build" (
    echo Limpando build anterior...
    rmdir /s /q "build"
)
if exist "dist" (
    echo Limpando dist anterior...
    rmdir /s /q "dist"
)

echo.
echo 🔨 Compilando o jogo...
echo Isso pode demorar alguns minutos...
echo.

REM Compilar o jogo
pyinstaller --onefile --windowed --name="Halloween_Game" --add-data="../craftpix-671123-free-halloween-2d-game-backgrounds;craftpix-671123-free-halloween-2d-game-backgrounds" --add-data="../craftpix-net-602985-free-wizard-sprite-sheets-pixel-art;craftpix-net-602985-free-wizard-sprite-sheets-pixel-art" jogo.py

if errorlevel 1 (
    echo.
    echo ❌ Erro durante a compilacao!
    echo Verifique se todos os arquivos estao presentes.
    pause
    exit /b 1
)

echo.
echo ✅ COMPILACAO CONCLUIDA COM SUCESSO!
echo.
echo O executavel foi criado em: dist\Halloween_Game.exe
echo.

REM Verificar se o arquivo foi criado
if exist "dist\Halloween_Game.exe" (
    echo ✓ Arquivo executavel criado com sucesso!
    echo Tamanho do arquivo:
    dir "dist\Halloween_Game.exe" | findstr "Halloween_Game.exe"
    echo.
    echo 🎮 Para testar o jogo compilado, execute:
    echo    dist\Halloween_Game.exe
    echo.
    echo 📦 Para distribuir o jogo, copie o arquivo:
    echo    dist\Halloween_Game.exe
) else (
    echo ❌ Arquivo executavel nao foi criado!
)

echo.
pause
