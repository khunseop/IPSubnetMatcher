@echo off
REM Conda 환경용 Windows 빌드 스크립트

echo ========================================
echo IP Network Matcher - Conda 빌드
echo ========================================
echo.

REM Conda 환경 확인
if "%CONDA_DEFAULT_ENV%"=="" (
    echo 경고: Conda 환경이 활성화되지 않았습니다.
    echo conda activate [환경이름] 을 먼저 실행하세요.
    echo.
    pause
    exit /b 1
) else (
    echo Conda 환경: %CONDA_DEFAULT_ENV%
    echo.
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

REM 파일 크기 확인
if exist "dist\IPNetworkMatcher.exe" (
    for %%A in ("dist\IPNetworkMatcher.exe") do (
        set size=%%~zA
        set /a sizeMB=%%~zA/1024/1024
        echo 파일 크기: !sizeMB! MB (%%~zA bytes)
    )
)

pause

