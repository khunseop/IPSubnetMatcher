# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 스펙 파일 - Windows 빌드용

block_cipher = None

import os
import sys

# customtkinter assets 경로 찾기 및 최적화
def find_customtkinter_assets():
    """
    customtkinter assets를 찾고 최적화합니다.
    사용하지 않는 테마 파일을 제외하여 용량을 줄입니다.
    """
    try:
        import customtkinter
        ctk_path = os.path.dirname(customtkinter.__file__)
        assets_path = os.path.join(ctk_path, 'assets')
        if not os.path.exists(assets_path):
            return []
        
        # 필요한 파일만 필터링 (사용하는 테마만 포함)
        # blue 테마만 사용하므로 다른 테마 제외 가능
        # 하지만 안전을 위해 모든 assets 포함 (필요시 수동으로 제외 가능)
        return [(assets_path, 'customtkinter/assets')]
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
        'openpyxl',
        'openpyxl.styles',
        'tkinter',
        'tkinter.filedialog',
        'threading',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 불필요한 표준 라이브러리 제외
        'matplotlib', 'numpy', 'scipy', 'pandas', 'pytest', 'unittest',
        'email', 'http', 'urllib3', 'requests', 'xmlrpc', 'distutils',
        'pydoc', 'doctest', 'pdb', 'bdb', 'curses', 'readline',
        # 불필요한 GUI 관련
        'tkinter.test', 'tkinter.tix', 'tkinter.scrolledtext',
        # 불필요한 데이터베이스
        'sqlite3', 'dbm', 'gdbm',
        # 불필요한 멀티미디어
        'audioop', 'wave', 'aifc', 'sunau',
        # 불필요한 인코딩
        'encodings.cp437', 'encodings.cp850', 'encodings.cp852',
        'encodings.cp855', 'encodings.cp856', 'encodings.cp857',
        'encodings.cp858', 'encodings.cp860', 'encodings.cp861',
        'encodings.cp862', 'encodings.cp863', 'encodings.cp864',
        'encodings.cp865', 'encodings.cp866', 'encodings.cp869',
        'encodings.cp874', 'encodings.cp875', 'encodings.cp932',
        'encodings.cp949', 'encodings.cp950', 'encodings.cp1006',
        'encodings.cp1026', 'encodings.cp1140', 'encodings.cp1250',
        'encodings.cp1251', 'encodings.cp1252', 'encodings.cp1253',
        'encodings.cp1254', 'encodings.cp1255', 'encodings.cp1256',
        'encodings.cp1257', 'encodings.cp1258', 'encodings.euc_jp',
        'encodings.euc_jis_2004', 'encodings.euc_jisx0213', 'encodings.euc_kr',
        'encodings.gb2312', 'encodings.gbk', 'encodings.gb18030',
        'encodings.hz', 'encodings.iso2022_jp', 'encodings.iso2022_jp_1',
        'encodings.iso2022_jp_2', 'encodings.iso2022_jp_2004',
        'encodings.iso2022_jp_3', 'encodings.iso2022_jp_ext', 'encodings.iso2022_kr',
        'encodings.latin_1', 'encodings.mbcs', 'encodings.palmos',
        'encodings.ptcp154', 'encodings.quopri_codec', 'encodings.raw_unicode_escape',
        'encodings.rot_13', 'encodings.shift_jis', 'encodings.shift_jis_2004',
        'encodings.shift_jisx0213', 'encodings.tis_620', 'encodings.unicode_escape',
        'encodings.utf_16', 'encodings.utf_16_be', 'encodings.utf_16_le',
        'encodings.utf_32', 'encodings.utf_32_be', 'encodings.utf_32_le',
        'encodings.utf_7', 'encodings.uu_codec', 'encodings.zlib_codec',
        # 불필요한 기타 모듈
        'lib2to3', 'pydoc_data', 'test', 'tests', 'distutils',
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
    strip=True,  # 디버그 심볼 제거로 용량 감소
    upx=True,  # UPX 압축 활성화 (UPX가 PATH에 있거나 upx_dir로 경로 지정 필요)
    # upx_dir=r'C:\UPX',  # UPX 경로 직접 지정 (PATH에 없을 경우 주석 해제하고 경로 수정)
    upx_exclude=[
        'vcruntime140.dll',  # Windows 런타임 DLL은 UPX 압축 제외 (호환성)
        'python*.dll',  # Python DLL은 UPX 압축 제외
    ],
    runtime_tmpdir=None,
    console=False,  # GUI 애플리케이션이므로 콘솔 창 숨김
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons8-비교-50.ico',  # 아이콘 파일 경로 지정 (Windows 실행 파일 아이콘)
)

