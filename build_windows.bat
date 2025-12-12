@echo off
REM Windows 빌드 스크립트

echo ========================================
echo IP Network Matcher - Windows 빌드
echo ========================================
echo.

REM PyInstaller 설치 확인
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller 설치 중...
    pip install pyinstaller
)

echo.
echo 빌드 시작...
echo.

REM 빌드 실행 (customtkinter assets 자동 포함)
pyinstaller build_windows.spec --clean --collect-all customtkinter

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
