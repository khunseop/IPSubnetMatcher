# 배포 가이드

이 문서는 IP Network Matcher 애플리케이션을 배포하기 위한 상세한 가이드를 제공합니다.

## 목차

- [빌드 환경 준비](#빌드-환경-준비)
- [Windows 실행 파일 빌드](#windows-실행-파일-빌드)
- [macOS 실행 파일 빌드](#macos-실행-파일-빌드)
- [Linux 실행 파일 빌드](#linux-실행-파일-빌드)
- [배포 패키징](#배포-패키징)
- [배포 체크리스트](#배포-체크리스트)

## 빌드 환경 준비

### 필수 요구사항

1. **Python 3.8 이상** 설치 확인
   ```bash
   python --version
   ```

2. **필수 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **PyInstaller 설치** (이미 requirements.txt에 포함됨)
   ```bash
   pip install pyinstaller
   ```

### 프로젝트 구조 확인

빌드 전에 다음 파일들이 있는지 확인하세요:
- `main.py` - 메인 진입점
- `build_windows.spec` - Windows 빌드 설정
- `icons8-비교-50.ico` - 애플리케이션 아이콘
- `core/`, `ui/`, `utils/` 디렉토리

## Windows 실행 파일 빌드

### 방법 1: 배치 파일 사용 (권장)

#### Windows Command Prompt
```cmd
build_windows.bat
```

#### Git Bash / WSL
```bash
bash build_windows.sh
```

### 방법 2: 수동 빌드

```bash
pyinstaller build_windows.spec --clean
```

### 빌드 결과

빌드가 성공하면 다음 위치에 실행 파일이 생성됩니다:
- `dist/IPNetworkMatcher.exe` - 단일 실행 파일

### 빌드 옵션 커스터마이징

`build_windows.spec` 파일을 수정하여 다음을 변경할 수 있습니다:

#### 실행 파일 이름 변경
```python
exe = EXE(
    ...
    name='YourAppName',  # 여기 변경
    ...
)
```

#### 아이콘 변경
```python
exe = EXE(
    ...
    icon='your-icon.ico',  # 여기 변경
    ...
)
```

#### 콘솔 창 표시 (디버깅용)
```python
exe = EXE(
    ...
    console=True,  # False에서 True로 변경
    ...
)
```

## macOS 실행 파일 빌드

### spec 파일 생성

```bash
pyinstaller --name=IPNetworkMatcher \
            --onefile \
            --windowed \
            --icon=icons8-비교-50.ico \
            --add-data="icons8-비교-50.ico:." \
            main.py
```

또는 `build_macos.spec` 파일을 생성하여 사용:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('icons8-비교-50.ico', '.')],
    hiddenimports=[
        'customtkinter',
        'openpyxl',
        'openpyxl.styles',
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons8-비교-50.ico',
)
```

### 빌드 실행

```bash
pyinstaller build_macos.spec --clean
```

### 코드 서명 (선택사항)

배포를 위해 코드 서명이 필요할 수 있습니다:

```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/IPNetworkMatcher.app
```

## Linux 실행 파일 빌드

### spec 파일 생성

`build_linux.spec` 파일을 생성:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'customtkinter',
        'openpyxl',
        'openpyxl.styles',
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

### 빌드 실행

```bash
pyinstaller build_linux.spec --clean
```

## 배포 패키징

### Windows 배포 패키지

1. **단일 실행 파일 배포**
   - `dist/IPNetworkMatcher.exe` 파일만 배포
   - 사용자는 실행 파일만 다운로드하여 실행 가능

2. **ZIP 패키지 생성**
   ```
   IPNetworkMatcher-v1.0.0-Windows.zip
   ├── IPNetworkMatcher.exe
   ├── README.md
   └── LICENSE
   ```

### macOS 배포 패키지

1. **DMG 파일 생성** (선택사항)
   ```bash
   # DMG 생성 도구 사용 (예: create-dmg)
   create-dmg --volname "IPNetworkMatcher" \
              --window-pos 200 120 \
              --window-size 800 400 \
              --icon-size 100 \
              --app-drop-link 600 185 \
              "IPNetworkMatcher.dmg" \
              "dist/IPNetworkMatcher.app"
   ```

2. **ZIP 패키지**
   ```
   IPNetworkMatcher-v1.0.0-macOS.zip
   ├── IPNetworkMatcher.app
   ├── README.md
   └── LICENSE
   ```

### Linux 배포 패키지

1. **AppImage 생성** (선택사항)
   - AppImageKit 사용

2. **DEB 패키지** (Debian/Ubuntu)
   - `dh_make` 및 `debuild` 사용

3. **RPM 패키지** (RedHat/CentOS)
   - `rpmbuild` 사용

## 배포 체크리스트

### 빌드 전 확인사항

- [ ] 모든 의존성이 `requirements.txt`에 포함되어 있는지 확인
- [ ] 아이콘 파일이 올바른 위치에 있는지 확인
- [ ] 버전 번호가 업데이트되었는지 확인
- [ ] README.md가 최신 상태인지 확인
- [ ] LICENSE 파일이 포함되어 있는지 확인

### 빌드 후 확인사항

- [ ] 실행 파일이 정상적으로 생성되었는지 확인
- [ ] 실행 파일이 다른 컴퓨터에서도 작동하는지 테스트
- [ ] 아이콘이 올바르게 표시되는지 확인
- [ ] 모든 기능이 정상 작동하는지 테스트
  - [ ] IP 입력 및 파싱
  - [ ] 매칭 분석
  - [ ] 엑셀 내보내기
  - [ ] 초기화 기능

### 배포 전 확인사항

- [ ] 실행 파일 크기가 적절한지 확인
- [ ] 바이러스 검사 통과 확인 (Windows)
- [ ] 코드 서명 완료 (macOS, 선택사항)
- [ ] 배포 패키지에 필요한 파일만 포함되었는지 확인
- [ ] 사용자 가이드 문서가 포함되었는지 확인

### 배포 후 확인사항

- [ ] 다운로드 링크가 정상 작동하는지 확인
- [ ] 설치 가이드가 명확한지 확인
- [ ] 사용자 피드백 수집 준비

## 문제 해결

### 빌드 실패

1. **모듈을 찾을 수 없음**
   ```bash
   # 모든 의존성 재설치
   pip install --upgrade -r requirements.txt
   ```

2. **아이콘 파일을 찾을 수 없음**
   - 아이콘 파일 경로 확인
   - `build_windows.spec`의 `datas` 섹션 확인

3. **실행 파일이 너무 큼**
   - 불필요한 모듈 제외
   - UPX 압축 활성화 확인

### 실행 파일 실행 오류

1. **Windows: "Windows에서 PC를 보호했습니다"**
   - 코드 서명 필요
   - 또는 사용자에게 "추가 정보" > "실행" 안내

2. **macOS: "확인되지 않은 개발자"**
   - 코드 서명 필요
   - 또는 보안 설정에서 허용 안내

3. **모듈 임포트 오류**
   - `hiddenimports`에 누락된 모듈 추가
   - `build_windows.spec` 수정 후 재빌드

## 추가 리소스

- [PyInstaller 공식 문서](https://pyinstaller.org/)
- [CustomTkinter 문서](https://customtkinter.tomschimansky.com/)
- [Python 패키징 가이드](https://packaging.python.org/)

---

**참고**: 이 가이드는 일반적인 배포 시나리오를 다룹니다. 특정 환경이나 요구사항에 따라 추가 설정이 필요할 수 있습니다.
