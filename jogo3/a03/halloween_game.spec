# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['jogo.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../craftpix-671123-free-halloween-2d-game-backgrounds', 'craftpix-671123-free-halloween-2d-game-backgrounds'),
        ('../craftpix-net-602985-free-wizard-sprite-sheets-pixel-art', 'craftpix-net-602985-free-wizard-sprite-sheets-pixel-art'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Halloween_Game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    cofile=None,
    icon=None,
    version=None,
    uac_admin=False,
    uac_uiaccess=False,
)
