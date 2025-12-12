# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 스펙 파일 - Windows 빌드용 (기본 설정)

block_cipher = None

import os

# customtkinter assets 경로 찾기 (.DS_Store 제외)
def find_customtkinter_assets():
    """customtkinter assets를 찾고 .DS_Store만 제외"""
    try:
        import customtkinter
        ctk_path = os.path.dirname(customtkinter.__file__)
        assets_path = os.path.join(ctk_path, 'assets')
        if os.path.exists(assets_path):
            # .DS_Store 제외하고 전체 포함
            filtered_files = []
            for root, dirs, files in os.walk(assets_path):
                # .DS_Store 파일 제외
                files = [f for f in files if f != '.DS_Store' and not f.startswith('._')]
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, ctk_path)
                    filtered_files.append((file_path, os.path.join('customtkinter', rel_path)))
            return filtered_files if filtered_files else [(assets_path, 'customtkinter/assets')]
    except:
        pass
    return []

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=find_customtkinter_assets() + [('icons8-비교-50.ico', '.')],
    hiddenimports=[
        'customtkinter',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'openpyxl',
        'tkinter',
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
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons8-비교-50.ico',
)
