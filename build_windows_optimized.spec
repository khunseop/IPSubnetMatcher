# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 스펙 파일 - Windows 빌드용 (최적화 버전: 폴더 모드)
# 폴더 모드는 단일 파일보다 용량이 작을 수 있습니다

block_cipher = None

import os
import sys

# customtkinter assets 경로 찾기 및 최적화
def find_customtkinter_assets():
    """
    customtkinter assets를 찾고 최적화합니다.
    blue 테마만 사용하므로 다른 테마 파일을 제외하여 용량을 줄입니다.
    """
    try:
        import customtkinter
        ctk_path = os.path.dirname(customtkinter.__file__)
        assets_path = os.path.join(ctk_path, 'assets')
        if not os.path.exists(assets_path):
            return []
        
        # blue 테마만 사용하므로 필요한 파일만 필터링
        files_to_include = []
        
        # assets 폴더 구조: assets/themes/blue/, assets/themes/dark-blue/, etc.
        themes_path = os.path.join(assets_path, 'themes')
        if os.path.exists(themes_path):
            # blue 테마만 포함
            blue_theme_path = os.path.join(themes_path, 'blue')
            if os.path.exists(blue_theme_path):
                for root, dirs, files in os.walk(blue_theme_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, ctk_path)
                        files_to_include.append((file_path, os.path.join('customtkinter', rel_path)))
            
            # 공통 assets (themes 외부의 파일들)
            for item in os.listdir(assets_path):
                item_path = os.path.join(assets_path, item)
                if os.path.isfile(item_path):
                    rel_path = os.path.relpath(item_path, ctk_path)
                    files_to_include.append((item_path, os.path.join('customtkinter', rel_path)))
                elif os.path.isdir(item_path) and item != 'themes':
                    # themes 외의 다른 폴더도 포함 (예: images 등)
                    for root, dirs, files in os.walk(item_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, ctk_path)
                            files_to_include.append((file_path, os.path.join('customtkinter', rel_path)))
        
        # 필터링된 파일이 있으면 반환, 없으면 전체 포함 (안전장치)
        if files_to_include:
            return files_to_include
        else:
            # 필터링 실패 시 전체 포함 (안전)
            return [(assets_path, 'customtkinter/assets')]
    except Exception as e:
        # 오류 발생 시 전체 포함 (안전)
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
    datas=find_customtkinter_assets() + [('icons8-비교-50.ico', '.')],
    hiddenimports=[
        'customtkinter',
        'customtkinter.windows',
        'customtkinter.windows.ctk_tk',
        'customtkinter.windows.ctk_frame',
        'customtkinter.windows.ctk_button',
        'customtkinter.windows.ctk_label',
        'customtkinter.windows.ctk_textbox',
        'customtkinter.windows.ctk_font',
        'PIL',
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk',
        'openpyxl',
        'openpyxl.styles',
        'openpyxl.workbook',
        'openpyxl.worksheet',
        'openpyxl.cell',
        'openpyxl.utils',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.font',
        'threading',
        'ipaddress',
        'json',
        're',
        'typing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'scipy', 'pandas', 'pytest', 'unittest',
        'email', 'http', 'urllib3', 'requests', 'xmlrpc', 'distutils',
        'pydoc', 'doctest', 'pdb', 'bdb', 'curses', 'readline',
        'tkinter.test', 'tkinter.tix', 'tkinter.scrolledtext',
        'sqlite3', 'dbm', 'gdbm',
        'audioop', 'wave', 'aifc', 'sunau',
        'openpyxl.chart', 'openpyxl.chartsheet', 'openpyxl.comments',
        'openpyxl.drawing', 'openpyxl.formula', 'openpyxl.packaging',
        'openpyxl.pivot', 'openpyxl.reader', 'openpyxl.writer',
        'encodings.cp437', 'encodings.cp850', 'encodings.cp852',
        'encodings.cp855', 'encodings.cp856', 'encodings.cp857',
        'encodings.cp858', 'encodings.cp860', 'encodings.cp861',
        'encodings.cp862', 'encodings.cp863', 'encodings.cp864',
        'encodings.cp865', 'encodings.cp866', 'encodings.cp869',
        'encodings.cp874', 'encodings.cp875', 'encodings.cp932',
        'encodings.cp949', 'encodings.cp950', 'encodings.cp1006',
        'encodings.cp1026', 'encodings.cp1140', 'encodings.cp1250',
        'encodings.cp1251', 'encodings.cp1253',
        'encodings.cp1254', 'encodings.cp1255', 'encodings.cp1256',
        'encodings.cp1257', 'encodings.cp1258', 'encodings.euc_jp',
        'encodings.euc_jis_2004', 'encodings.euc_jisx0213', 'encodings.euc_kr',
        'encodings.gb2312', 'encodings.gbk', 'encodings.gb18030',
        'encodings.hz', 'encodings.iso2022_jp', 'encodings.iso2022_jp_1',
        'encodings.iso2022_jp_2', 'encodings.iso2022_jp_2004',
        'encodings.iso2022_jp_3', 'encodings.iso2022_jp_ext', 'encodings.iso2022_kr',
        'encodings.palmos', 'encodings.ptcp154', 'encodings.quopri_codec',
        'encodings.raw_unicode_escape', 'encodings.rot_13', 'encodings.shift_jis',
        'encodings.shift_jis_2004', 'encodings.shift_jisx0213', 'encodings.tis_620',
        'encodings.utf_16', 'encodings.utf_16_be', 'encodings.utf_16_le',
        'encodings.utf_32', 'encodings.utf_32_be', 'encodings.utf_32_le',
        'encodings.utf_7', 'encodings.uu_codec', 'encodings.zlib_codec',
        'lib2to3', 'pydoc_data', 'test', 'tests',
        'setuptools', 'wheel', 'pip',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 폴더 모드 (단일 파일보다 작을 수 있음)
exe = EXE(
    pyz,
    a.scripts,
    [],  # 빈 리스트로 변경하여 폴더 모드 활성화
    exclude_binaries=True,  # 바이너리를 별도로 분리
    name='IPNetworkMatcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[
        'vcruntime140.dll',
        'python*.dll',
    ],
    runtime_tmpdir=None,
    console=False,  # GUI 애플리케이션이므로 콘솔 창 숨김
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons8-비교-50.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[
        'vcruntime140.dll',
        'python*.dll',
    ],
    name='IPNetworkMatcher',
)

