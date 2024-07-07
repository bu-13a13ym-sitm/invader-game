# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['invader-game.py'],
    pathex=[
        '/home/ub723356/invader-game/venv/lib/python3.11/site-packages',
        '/home/ub723356/invader-game/venv/local/lib/python3.11/dist-packages',
        '/home/ub723356/invader-game/venv/lib/python3/dist-packages',
        '/home/ub723356/invader-game/venv/lib/python3.11/dist-packages'
    ],
    binaries=[],
    datas=[],
    hiddenimports=[
        'RPi.GPIO',
        'gpiozero.pins.rpigpio',
        'gpiozero.pins.lgpio',
        'gpiozero.pins.pigpio',
        'gpiozero.pins.native',
        'lgpio'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='invader-game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='invader-game',
)
