# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ui_home.py',
    'dialog\\about.py','dialog\\change_config.py','dialog\\create_server.py','dialog\\load_server.py','dialog\\manage_server.py','dialog\\start_server.py','dialog\\list\\ban_ip.py','dialog\\list\\ban_player.py','dialog\\list\\op.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='McServerPanel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='image/Conditional_Repeating_Command_Block.ico',
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
    name='ui_home',
)
