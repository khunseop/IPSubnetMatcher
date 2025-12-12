# UPX 설치 및 설정 가이드

## UPX란?
UPX는 실행 파일을 압축하는 도구로, PyInstaller로 빌드한 실행 파일의 용량을 크게 줄일 수 있습니다.

## Windows 설치 방법

### 방법 1: PATH 환경변수에 추가 (권장)

1. **UPX 압축 해제**
   - 다운로드한 UPX 압축 파일을 원하는 위치에 압축 해제 (예: `C:\UPX`)

2. **환경변수에 추가**
   - `Win + R` 키를 누르고 `sysdm.cpl` 입력 후 Enter
   - "고급" 탭 → "환경 변수" 클릭
   - "시스템 변수"에서 "Path" 선택 → "편집" 클릭
   - "새로 만들기" 클릭 → UPX 폴더 경로 입력 (예: `C:\UPX`)
   - 모든 창에서 "확인" 클릭

3. **새 터미널에서 확인**
   - 새로운 명령 프롬프트 또는 PowerShell 열기
   - 다음 명령어로 확인:
     ```cmd
     upx --version
     ```
   - 버전 정보가 나오면 성공!

4. **PyInstaller 사용**
   - 이제 `build_windows.spec` 파일의 `upx=True` 설정이 자동으로 작동합니다.

### 방법 2: spec 파일에서 직접 경로 지정

PATH에 추가하지 않고도 사용할 수 있습니다.

1. **UPX 압축 해제**
   - 원하는 위치에 압축 해제 (예: `C:\Tools\UPX`)

2. **spec 파일 수정**
   - `build_windows.spec` 파일에서 UPX 경로를 직접 지정:
     ```python
     exe = EXE(
         ...
         upx=True,
         upx_dir=r'C:\Tools\UPX',  # UPX 경로 직접 지정
         ...
     )
     ```

### 방법 3: Chocolatey 사용 (가장 간단)

```cmd
choco install upx
```

이 방법은 자동으로 PATH에 등록됩니다.

## 확인 방법

빌드 시 PyInstaller가 UPX를 찾으면 다음과 같은 메시지가 나타납니다:
```
INFO: UPX is available.
```

UPX를 찾지 못하면:
```
WARNING: UPX is not available.
```

## 문제 해결

### UPX를 찾을 수 없다는 오류
1. 새 터미널을 열어서 환경변수 변경사항 적용
2. `upx --version` 명령어로 UPX가 인식되는지 확인
3. spec 파일에서 `upx_dir`로 직접 경로 지정

### UPX 압축 오류 발생 시
일부 DLL은 UPX 압축과 호환되지 않을 수 있습니다. `upx_exclude`에 추가하세요:
```python
upx_exclude=[
    'vcruntime140.dll',
    'python*.dll',
    '문제가_있는_파일.dll',
]
```

### UPX 없이 빌드하고 싶을 때
`build_windows.spec` 파일에서:
```python
upx=False,  # UPX 사용 안 함
```

## macOS/Linux 설치

**macOS:**
```bash
brew install upx
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install upx
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install upx
```

## 참고
- UPX 공식 사이트: https://upx.github.io/
- GitHub 릴리스: https://github.com/upx/upx/releases

