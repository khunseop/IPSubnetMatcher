# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 스펙 파일 - Windows 빌드용

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
        
        # 제외할 파일 패턴 (macOS 메타데이터 파일 등)
        exclude_patterns = ['.DS_Store', '._', 'Thumbs.db']
        
        def should_exclude(filename):
            """파일명이 제외 패턴에 해당하는지 확인"""
            for pattern in exclude_patterns:
                if filename.startswith(pattern) or filename == pattern:
                    return True
            return False
        
        # assets 폴더 구조: assets/themes/blue/, assets/themes/dark-blue/, etc.
        themes_path = os.path.join(assets_path, 'themes')
        if os.path.exists(themes_path):
            # blue 테마만 포함
            blue_theme_path = os.path.join(themes_path, 'blue')
            if os.path.exists(blue_theme_path):
                for root, dirs, files in os.walk(blue_theme_path):
                    # .DS_Store가 있는 디렉토리도 제외
                    dirs[:] = [d for d in dirs if not should_exclude(d)]
                    for file in files:
                        if not should_exclude(file):
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, ctk_path)
                            files_to_include.append((file_path, os.path.join('customtkinter', rel_path)))
            
            # 공통 assets (themes 외부의 파일들)
            for item in os.listdir(assets_path):
                if should_exclude(item):
                    continue
                item_path = os.path.join(assets_path, item)
                if os.path.isfile(item_path):
                    rel_path = os.path.relpath(item_path, ctk_path)
                    files_to_include.append((item_path, os.path.join('customtkinter', rel_path)))
                elif os.path.isdir(item_path) and item != 'themes':
                    # themes 외의 다른 폴더도 포함 (예: images 등)
                    for root, dirs, files in os.walk(item_path):
                        # .DS_Store가 있는 디렉토리도 제외
                        dirs[:] = [d for d in dirs if not should_exclude(d)]
                        for file in files:
                            if not should_exclude(file):
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
        # 오류 발생 시 전체 포함하되 .DS_Store는 제외 (안전)
        try:
            import customtkinter
            ctk_path = os.path.dirname(customtkinter.__file__)
            assets_path = os.path.join(ctk_path, 'assets')
            if os.path.exists(assets_path):
                # 전체 포함하되 .DS_Store는 제외하는 방법
                # PyInstaller의 Tree 함수를 사용하거나 필터링된 리스트 반환
                filtered_files = []
                exclude_patterns = ['.DS_Store', '._', 'Thumbs.db']
                for root, dirs, files in os.walk(assets_path):
                    dirs[:] = [d for d in dirs if not any(d.startswith(p) or d == p for p in exclude_patterns)]
                    for file in files:
                        if not any(file.startswith(p) or file == p for p in exclude_patterns):
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
    datas=find_customtkinter_assets() + [('icons8-비교-50.ico', '.')],  # customtkinter assets 및 아이콘 파일 포함
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
        # openpyxl 최소한만 포함
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
        # 불필요한 표준 라이브러리 제외 (기본 인코딩은 제외하지 않음)
        'matplotlib', 'numpy', 'scipy', 'pandas', 'pytest', 'unittest',
        'email', 'http', 'urllib3', 'requests', 'xmlrpc', 'distutils',
        'pydoc', 'doctest', 'pdb', 'bdb', 'curses', 'readline',
        # 불필요한 GUI 관련
        'tkinter.test', 'tkinter.tix', 'tkinter.scrolledtext',
        # 불필요한 데이터베이스
        'sqlite3', 'dbm', 'gdbm',
        # 불필요한 멀티미디어
        'audioop', 'wave', 'aifc', 'sunau',
        # openpyxl 불필요한 부분 제외
        'openpyxl.chart', 'openpyxl.chartsheet', 'openpyxl.comments',
        'openpyxl.drawing', 'openpyxl.formula', 'openpyxl.packaging',
        'openpyxl.pivot', 'openpyxl.reader', 'openpyxl.writer',
        # 일부 불필요한 인코딩만 제외 (기본 인코딩은 유지)
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
        # 불필요한 기타 모듈
        'lib2to3', 'pydoc_data', 'test', 'tests',
        'setuptools', 'wheel', 'pip',
    ],
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
    strip=False,  # 디버깅용으로 strip 비활성화 (오류 해결 후 True로 변경 가능)
    upx=True,  # UPX 압축 활성화 (UPX가 PATH에 있거나 upx_dir로 경로 지정 필요)
    # upx_dir=r'C:\UPX',  # UPX 경로 직접 지정 (PATH에 없을 경우 주석 해제하고 경로 수정)
    upx_exclude=[
        'vcruntime140.dll',  # Windows 런타임 DLL은 UPX 압축 제외 (호환성)
        'python*.dll',  # Python DLL은 UPX 압축 제외
    ],
    runtime_tmpdir=None,
    console=True,  # 디버깅용 콘솔 활성화 (오류 확인 후 False로 변경 가능)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons8-비교-50.ico',  # 아이콘 파일 경로 지정 (Windows 실행 파일 아이콘)
)

