# 빌드 문제 해결 가이드

## "failed to start embedded python interpreter" 오류

이 오류는 PyInstaller가 Python 인터프리터를 시작하지 못할 때 발생합니다.

### 해결 방법

#### 1. 필요한 모듈 추가 확인

`build_windows.spec` 파일의 `hiddenimports`에 다음이 포함되어 있는지 확인:
- `PIL` (Pillow)
- `customtkinter` 관련 모듈
- `tkinter` 관련 모듈

#### 2. 인코딩 모듈 확인

기본 인코딩 모듈은 제외하지 마세요:
- `encodings.utf_8` (필수)
- `encodings.ascii` (필수)
- `encodings.cp1252` (Windows 기본)

#### 3. 콘솔 모드로 디버깅

`build_windows.spec`에서:
```python
console=True,  # 오류 메시지 확인
```

빌드 후 실행 파일을 실행하면 콘솔 창에 상세한 오류 메시지가 표시됩니다.

#### 4. 빌드 캐시 삭제

```bash
# build와 dist 폴더 삭제 후 재빌드
rmdir /s /q build dist
pyinstaller build_windows.spec --clean
```

#### 5. 최소한의 excludes로 테스트

문제가 계속되면 `excludes` 리스트를 비우고 테스트:
```python
excludes=[],  # 일단 모두 포함하여 테스트
```

작동 확인 후 필요한 것만 제외하세요.

#### 6. 가상환경에서 깨끗하게 재설치

```bash
# 새 가상환경 생성
python -m venv venv_clean
venv_clean\Scripts\activate

# 패키지 재설치
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# 빌드
pyinstaller build_windows.spec --clean
```

## 일반적인 빌드 오류

### "PYI 22112 Error: failed to extract customtkinter\asset\DS_store"

이 오류는 macOS의 `.DS_Store` 파일이 Windows 빌드에 포함되어 발생합니다.

**해결 방법:**
1. `build_windows.spec` 파일이 최신 버전인지 확인 (이미 수정됨)
2. 빌드 캐시 삭제 후 재빌드:
   ```cmd
   rmdir /s /q build dist
   pyinstaller build_windows.spec --clean
   ```

**원인:**
- `.DS_Store`는 macOS의 폴더 메타데이터 파일입니다
- Windows에서는 필요하지 않고 PyInstaller가 추출할 수 없어 오류가 발생합니다
- `find_customtkinter_assets()` 함수에서 자동으로 제외하도록 수정되었습니다

**수동으로 확인:**
만약 문제가 계속되면, conda 환경의 customtkinter 패키지에서 직접 `.DS_Store` 파일을 삭제할 수 있습니다:
```bash
# conda 환경의 customtkinter assets 폴더에서 .DS_Store 찾기
find $CONDA_PREFIX/lib/python*/site-packages/customtkinter/assets -name ".DS_Store" -delete
```

### "ModuleNotFoundError"

해결:
1. `hiddenimports`에 누락된 모듈 추가
2. `--collect-all` 옵션 사용 (예: `--collect-all customtkinter`)

### "DLL load failed"

해결:
1. Visual C++ Redistributable 설치 확인
2. Python 버전과 호환되는 PyInstaller 사용
3. `upx_exclude`에 문제 DLL 추가

### 실행 파일이 너무 느림

해결:
1. `--onefile` 대신 폴더 모드 사용
2. `upx=False`로 변경 (UPX 압축 해제)
3. `strip=False`로 변경 (디버그 정보 유지)

## 디버깅 팁

### 1. 상세 로그 확인

```bash
pyinstaller build_windows.spec --log-level=DEBUG
```

### 2. 임시 파일 확인

빌드 후 `build/IPNetworkMatcher/` 폴더에서 누락된 파일 확인

### 3. 의존성 확인

```bash
# 프로젝트에서 사용하는 모든 import 확인
python -c "import main; import sys; print(sys.modules.keys())"
```

## 성공적인 빌드 후

오류가 해결되면 다시 최적화:
1. `console=False`로 변경
2. `strip=True`로 변경
3. 필요한 모듈만 `excludes`에 추가

