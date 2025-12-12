@echo off
REM Windows 빌드 스크립트

echo ========================================
echo IP Network Matcher - Windows 빌드
echo ========================================
echo.

REM 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

REM PyInstaller 설치 확인
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller 설치 중...
    pip install pyinstaller
)

REM UPX 확인 (선택사항)
where upx >nul 2>&1
if errorlevel 1 (
    echo.
    echo 참고: UPX가 설치되지 않았습니다. (선택사항)
    echo UPX 설치 시 실행 파일 용량이 더 작아집니다.
    echo 설치 방법: UPX_SETUP.md 파일 참조
    echo.
) else (
    echo UPX 발견됨 - 압축 활성화
)

echo.
echo 빌드 시작...
echo.

REM 빌드 실행
pyinstaller build_windows.spec --clean

if errorlevel 1 (
    echo.
    echo 빌드 실패!
    pause
    exit /b 1
)

echo.
echo ========================================
echo 빌드 완료!
echo ========================================
echo.
echo 실행 파일 위치: dist\IPNetworkMatcher.exe
echo.
pause

