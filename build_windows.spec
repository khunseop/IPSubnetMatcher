# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 스펙 파일 - Windows 빌드용

block_cipher = None

import os
import sys

# customtkinter assets 경로 찾기
def find_customtkinter_assets():
    try:
        import customtkinter
        ctk_path = os.path.dirname(customtkinter.__file__)
        assets_path = os.path.join(ctk_path, 'assets')
        if os.path.exists(assets_path):
            return [(assets_path, 'customtkinter/assets')]
    except:
        pass
    return []

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=find_customtkinter_assets(),  # customtkinter assets 포함
    hiddenimports=[
        'customtkinter',
        'openpyxl',
        'openpyxl.styles',
        'tkinter',
        'tkinter.filedialog',
        'threading',
    ],
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
    name='IPNetworkMatcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 애플리케이션이므로 콘솔 창 숨김
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 아이콘 파일이 있으면 경로 지정
)

