#!/bin/bash
# Windows 빌드 스크립트 (WSL 또는 Git Bash에서 사용)

echo "========================================"
echo "IP Network Matcher - Windows 빌드"
echo "========================================"
echo ""

# PyInstaller 설치 확인
python -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "PyInstaller 설치 중..."
    pip install pyinstaller
fi

echo ""
echo "빌드 시작..."
echo ""

# 빌드 실행
pyinstaller build_windows.spec --clean

if [ $? -ne 0 ]; then
    echo ""
    echo "빌드 실패!"
    exit 1
fi

echo ""
echo "========================================"
echo "빌드 완료!"
echo "========================================"
echo ""
echo "실행 파일 위치: dist/IPNetworkMatcher.exe"
echo ""
