@echo off
REM Nuitka 빌드 스크립트 - Windows용
REM UPX 압축 포함

echo ========================================
echo IP Network Matcher - Nuitka 빌드 (UPX 포함)
echo ========================================
echo.

REM 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM Nuitka 설치 확인
python -c "import nuitka" 2>nul
if errorlevel 1 (
    echo Nuitka 설치 중...
    pip install nuitka
)

REM UPX 설치 확인 (선택사항)
where upx >nul 2>&1
if errorlevel 1 (
    echo.
    echo 경고: UPX가 설치되지 않았습니다.
    echo UPX 없이 빌드합니다. (용량이 더 클 수 있습니다)
    echo UPX 설치: choco install upx 또는 https://upx.github.io/
    echo.
    set UPX_OPTION=
) else (
    echo UPX 발견됨 - 압축 활성화
    set UPX_OPTION=--plugin-enable=upx --upx-binary=upx --upx-exclude=vcruntime140.dll --upx-exclude=python*.dll
)

echo.
echo 빌드 시작...
echo.

REM Nuitka 빌드 실행
python -m nuitka --standalone --onefile --windows-disable-console ^
    --remove-output ^
    --lto=yes ^
    %UPX_OPTION% ^
    --include-package=customtkinter ^
    --include-package=openpyxl ^
    --include-data-dir=customtkinter/assets=customtkinter/assets ^
    --windows-icon-from-ico=icons8-비교-50.ico ^
    main.py

if errorlevel 1 (
    echo.
    echo 빌드 실패!
    echo.
    echo UPX 오류가 발생한 경우, UPX 없이 빌드해보세요:
    echo python -m nuitka --standalone --onefile --windows-disable-console --include-package=customtkinter --include-package=openpyxl main.py
    exit /b 1
)

echo.
echo ========================================
echo 빌드 완료!
echo ========================================
echo.
echo 실행 파일 위치: main.dist\main.exe
echo.

