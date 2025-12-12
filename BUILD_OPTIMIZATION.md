# 빌드 최적화 가이드

## 실행 파일 용량 최적화 방법

PyInstaller로 빌드한 실행 파일의 용량을 줄이기 위한 최적화 방법들을 정리했습니다.

## 적용된 최적화

### 1. 불필요한 모듈 제외
`build_windows.spec` 파일의 `excludes` 리스트에 다음 모듈들을 제외했습니다:
- 테스트/개발 도구: `pytest`, `unittest`, `pdb`, `doctest`
- 데이터 분석: `matplotlib`, `numpy`, `scipy`, `pandas`
- 네트워크: `http`, `urllib3`, `requests`
- 불필요한 인코딩: 사용하지 않는 인코딩 모듈들
- 기타: `lib2to3`, `pydoc_data`, `setuptools`, `wheel`, `pip`

### 2. 디버그 심볼 제거
`strip=True`로 설정하여 디버그 심볼을 제거했습니다.

### 3. UPX 압축 활성화
`upx=True`로 설정하여 실행 파일을 압축했습니다. (UPX가 설치되어 있어야 함)

## 추가 최적화 방법

### 방법 1: UPX 설치 및 사용
UPX는 실행 파일을 압축하는 도구입니다. 설치하면 자동으로 압축됩니다.

**Windows:**
```bash
# Chocolatey 사용
choco install upx

# 또는 수동 다운로드
# https://upx.github.io/ 에서 다운로드
```

### 방법 2: 폴더 모드 사용 (더 작은 용량)
단일 실행 파일 대신 폴더 모드로 빌드하면 용량이 더 작아질 수 있습니다.

`build_windows.spec` 파일의 `EXE` 섹션을 다음과 같이 수정:

```python
exe = EXE(
    pyz,
    a.scripts,
    [],  # 빈 리스트로 변경
    exclude_binaries=True,  # 추가
    name='IPNetworkMatcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    icon='icons8-비교-50.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='IPNetworkMatcher',
)
```

단점: 실행 파일과 함께 여러 DLL 파일이 생성됩니다.

### 방법 3: 가상환경에서 최소한의 패키지만 설치
빌드 전에 깨끗한 가상환경을 만들고 필요한 패키지만 설치:

```bash
python -m venv venv_build
source venv_build/bin/activate  # Windows: venv_build\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 방법 4: customtkinter 테마 최적화
현재 `blue` 테마만 사용하므로, 다른 테마 파일을 제외할 수 있습니다.

`find_customtkinter_assets()` 함수를 수정하여 필요한 파일만 포함:

```python
def find_customtkinter_assets():
    try:
        import customtkinter
        ctk_path = os.path.dirname(customtkinter.__file__)
        assets_path = os.path.join(ctk_path, 'assets')
        if not os.path.exists(assets_path):
            return []
        
        # blue 테마만 포함
        import glob
        files_to_include = []
        for root, dirs, files in os.walk(assets_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, ctk_path)
                # blue 테마 관련 파일만 포함
                if 'blue' in rel_path.lower() or file.endswith(('.png', '.svg')):
                    files_to_include.append((file_path, os.path.join('customtkinter', rel_path)))
        
        return files_to_include
    except:
        pass
    return []
```

주의: 이 방법은 테스트가 필요하며, 실행 시 오류가 발생할 수 있습니다.

### 방법 5: Python 버전 최적화
Python 3.11 이상을 사용하면 더 작은 실행 파일을 생성할 수 있습니다.

### 방법 6: Nuitka 사용 (대안)
PyInstaller 대신 Nuitka를 사용하면 더 작은 실행 파일을 만들 수 있습니다.

**기본 Nuitka 빌드:**
```bash
pip install nuitka
python -m nuitka --standalone --onefile --windows-disable-console --include-package=customtkinter --include-package=openpyxl main.py
```

**Nuitka + UPX 압축 (동시 사용 가능):**
Nuitka는 UPX 플러그인을 지원합니다 (버전 0.7 이상).

```bash
# UPX 플러그인 활성화
python -m nuitka --standalone --onefile --windows-disable-console \
  --plugin-enable=upx \
  --upx-binary=upx \
  --include-package=customtkinter \
  --include-package=openpyxl \
  main.py
```

**주의사항:**
- Windows 시스템 DLL (`vcruntime140.dll` 등)은 UPX 압축에서 제외해야 합니다
- 압축 비율이 낮으면 `NotCompressibleException` 오류가 발생할 수 있습니다
- 호환성 문제가 발생하면 UPX 없이 빌드하거나 시스템 DLL을 제외하세요

**시스템 DLL 제외 예시:**
```bash
python -m nuitka --standalone --onefile --windows-disable-console \
  --plugin-enable=upx \
  --upx-exclude=vcruntime140.dll \
  --upx-exclude=python*.dll \
  --include-package=customtkinter \
  --include-package=openpyxl \
  main.py
```

**Nuitka 추가 최적화 옵션:**
```bash
python -m nuitka --standalone --onefile --windows-disable-console \
  --plugin-enable=upx \
  --lto=yes \  # Link Time Optimization
  --remove-output \  # 빌드 후 임시 파일 제거
  --include-package=customtkinter \
  --include-package=openpyxl \
  main.py
```

## 예상 용량 감소

### PyInstaller 기준:
- 기본 최적화: **20-30% 감소**
- UPX 압축 추가: **40-50% 감소**
- customtkinter 테마 최적화: **추가 5-10% 감소** (blue 테마만 포함)
- openpyxl 모듈 제외: **추가 2-5% 감소**
- 폴더 모드: **30-40% 감소** (단일 파일 대비, 전체 폴더 크기는 비슷하지만 실행 파일만 작음)

### 현재 18MB에서 추가로 줄일 수 있는 방법:
1. **customtkinter 테마 최적화**: ~1-2MB 감소 (이미 적용됨)
2. **openpyxl 모듈 제외**: ~0.5-1MB 감소 (이미 적용됨)
3. **폴더 모드 사용**: 실행 파일만 ~5-8MB로 감소 (전체 폴더는 비슷)
4. **UPX 압축**: ~30-40% 추가 감소 가능

### Nuitka 기준:
- 기본 빌드: **PyInstaller 대비 10-20% 작음**
- Nuitka + UPX: **PyInstaller + UPX 대비 5-15% 작음**
- Nuitka + LTO: **추가 5-10% 감소**

## 빌드 후 확인

빌드 후 다음을 확인하세요:

1. 실행 파일 크기 확인
2. 실행 파일이 정상 작동하는지 테스트
3. 모든 기능이 정상 작동하는지 확인

## 문제 해결

### UPX 오류 발생 시
UPX가 설치되지 않았거나 호환성 문제가 있을 수 있습니다. `upx=False`로 변경하거나 `upx_exclude`에 문제가 있는 DLL을 추가하세요.

### 실행 파일이 작동하지 않을 때
일부 모듈이 과도하게 제외되었을 수 있습니다. `excludes` 리스트에서 해당 모듈을 제거하세요.

### 용량이 여전히 큰 경우
1. `dist` 폴더의 전체 크기 확인 (단일 파일만 확인하지 말고)
2. `build` 폴더 삭제 후 재빌드
3. 가상환경에서 깨끗하게 재설치 후 빌드

